import os
from datetime import datetime
from typing import Optional, List
from urllib.parse import urljoin
import requests
import numpy
import logging

from ..concurrency.query_pool import QueryPool
from .interface import DatasetId
from ..utils.maxsizedict import MaxSizeDict
from ..utils.url import normalize_url
from . import defaults

logger = logging.getLogger(__name__)


class IcatInvestigationClient:
    """Client for the investigation part of the ICAT+ REST API.

    An "investigation" is a time slot assigned to a particular proposal
    at a particular beamline.

    REST API docs:
    https://icatplus.esrf.fr/api-docs/

    The ICAT+ server project:
    https://gitlab.esrf.fr/icat/icat-plus/-/blob/master/README.md
    """

    DEFAULT_SCHEME = "https"

    def __init__(
        self,
        url: str,
        api_key: Optional[str] = None,
        timeout: Optional[float] = None,
    ):
        if api_key is None:
            api_key = defaults.ELOGBOOK_TOKEN
        url = normalize_url(url, default_scheme=self.DEFAULT_SCHEME)

        path = f"dataacquisition/{api_key}/investigation"
        query = "?instrumentName={beamline}&investigationName={proposal}"
        self._investigation_url = urljoin(url, path + query)

        path = f"dataacquisition/{api_key}/dataset"
        query = "?investigationId={investigation_id}"
        self._dataset_url = urljoin(url, path + query)

        self.raise_error = False
        self.__query_pool = QueryPool(timeout=timeout, maxqueries=20)
        self.__investigation_info = MaxSizeDict(maxsize=20)

    @property
    def timeout(self):
        return self.__query_pool.timeout

    @timeout.setter
    def timeout(self, value: Optional[float] = None):
        self.__query_pool.timeout = value

    def _get_with_response_parsing(
        self, url: str, timeout: Optional[float] = None
    ) -> Optional[list]:
        """Return `None` means the information is not available at this moment.
        An empty list means that an error has occured or an actual empty list
        is returned.
        """
        try:
            response = self.__query_pool.execute(
                requests.get, args=(url,), timeout=timeout, default=None
            )
        except requests.exceptions.ReadTimeout:
            return None
        except Exception as e:
            if self.raise_error:
                raise
            logger.exception(e)
            return None
        if response is None:
            return None
        if self.raise_error:
            response.raise_for_status()
        elif not response.ok:
            logger.error("%s: %s", response, response.text)
        if response.ok:
            return response.json()
        else:
            return list()

    def investigation_info(
        self,
        beamline: str,
        proposal: str,
        date: Optional[datetime] = None,
        allow_open_ended: bool = True,
        timeout: Optional[float] = None,
    ) -> Optional[dict]:
        """An investigation is defined by a time slot. Find an investigation (if any)
        for a beamline, proposal and date ("now" when not provided). When there is
        more than one investigation, select the closest one started before or at the date.
        If there is no such investigation, get the closest investigation which starts after the date.
        """
        investigation_key = beamline, proposal, date
        ninfo = self.__investigation_info.get(investigation_key)
        if ninfo is not None:
            return ninfo

        # Get all investigations for this proposal and beamline
        url = self._investigation_url.format(beamline=beamline, proposal=proposal)
        investigations = self._get_with_response_parsing(url, timeout=timeout)
        if investigations is None:
            return None  # not available at the moment

        # Select investigation
        investigation = _select_investigation(
            investigations, date=date, allow_open_ended=allow_open_ended
        )
        if investigation is None:
            return dict()  # no valid investigation found

        # Normalize information
        for key in ["parameters", "visitId"]:
            investigation.pop(key, None)
        ninfo = dict()
        ninfo["proposal"] = investigation.pop("name", None)
        ninfo["beamline"] = investigation.pop("instrument", dict()).get("name", None)
        ninfo.update(investigation)
        ninfo[
            "e-logbook"
        ] = f"https://data.esrf.fr/investigation/{investigation['id']}/events"
        ninfo[
            "data portal"
        ] = f"https://data.esrf.fr/investigation/{investigation['id']}/datasets"

        self.__investigation_info[investigation_key] = ninfo
        return ninfo

    def _investigation_id(
        self,
        beamline: str,
        proposal: str,
        date: Optional[datetime] = None,
        allow_open_ended: bool = True,
        timeout: Optional[float] = None,
    ) -> Optional[int]:
        info = self.investigation_info(
            beamline=beamline,
            proposal=proposal,
            date=date,
            allow_open_ended=allow_open_ended,
            timeout=timeout,
        )
        if info is None:
            return None
        return info.get("id", None)

    def registered_dataset_ids(
        self,
        beamline: str,
        proposal: str,
        date: Optional[datetime] = None,
        allow_open_ended: bool = True,
        timeout: Optional[float] = None,
    ) -> Optional[List[DatasetId]]:
        investigation_id = self._investigation_id(
            beamline=beamline,
            proposal=proposal,
            date=date,
            allow_open_ended=allow_open_ended,
            timeout=timeout,
        )
        if investigation_id is None:
            return None
        url = self._dataset_url.format(investigation_id=investigation_id)
        datasets = self._get_with_response_parsing(url, timeout=timeout)
        if datasets is None:
            return None
        return [self._icat_dataset_to_datasetid(dataset) for dataset in datasets]

    @staticmethod
    def _icat_dataset_to_datasetid(dataset: dict) -> DatasetId:
        location = dataset["location"]
        location, name = os.path.split(location)
        while location and not name:
            location, name = os.path.split(location)
        return DatasetId(name=name, path=dataset["location"])


def _select_investigation(
    investigations: List[dict],
    date: Optional[datetime] = None,
    allow_open_ended: bool = True,
) -> Optional[dict]:
    """When `date` is not provided we take it to be "now".

    This method returns the last investigation that contains
    the date or has a start/end closest to the date. The
    investigations are ordered from first to last created.

    Optionally all open-ended investigations can be ignored.
    Open-ended investigations have a start date but no end date.
    These investigations are created by sending dataset or
    investigation messages with start dates 48h outside any
    official investigation.
    """
    # Select valid investigations
    if allow_open_ended:
        valid = [
            investigation
            for investigation in investigations
            if investigation.get("startDate")
        ]
    else:
        valid = [
            investigation
            for investigation in investigations
            if investigation.get("startDate") and investigation.get("endDate")
        ]
    if not valid:
        return
    if len(valid) == 1:
        return valid[0]

    if date is None:
        date = datetime.now()
    date = date.astimezone()

    # Sorted by creation order
    valid_sorted = sorted(valid, key=lambda investigation: investigation["id"])

    # Seconds between date and start/end of each investigation
    n = len(valid_sorted)
    startdiff = numpy.zeros(n)
    enddiff = numpy.full(n, numpy.inf)
    for i, investigation in enumerate(valid_sorted):
        startdate = _tz_aware_fromisoformat(investigation["startDate"])
        startdiff[i] = (date - startdate).total_seconds()
        enddate = investigation.get("endDate")
        if enddate is not None:
            enddate = _tz_aware_fromisoformat(enddate)
            enddiff[i] = (enddate - date).total_seconds()

    # Last investigation which contains the date
    contains_date = (startdiff >= 0) & (enddiff >= 0)
    if contains_date.any():
        i = numpy.argwhere(contains_date)[-1][0]
        return valid_sorted[i]

    # Last investigation with the closest start or end date
    startdiff = numpy.abs(startdiff)
    enddiff = numpy.abs(enddiff)
    istart = numpy.argmin(startdiff)
    iend = numpy.argmin(enddiff)
    min_startdiff = startdiff[istart]
    min_enddiff = enddiff[iend]
    if min_startdiff < min_enddiff:
        return valid_sorted[istart]
    if min_startdiff > min_enddiff:
        return valid_sorted[iend]
    return valid_sorted[max(istart, iend)]


def _tz_aware_fromisoformat(date: str) -> datetime:
    return datetime.fromisoformat(date).astimezone()
