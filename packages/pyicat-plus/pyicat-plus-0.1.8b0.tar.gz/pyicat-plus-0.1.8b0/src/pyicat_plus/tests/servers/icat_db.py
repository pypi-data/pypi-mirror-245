import os
import json
import logging
from datetime import datetime
from typing import Optional, Dict, List


logger = logging.getLogger(__name__)


class IcatDb:
    def __init__(self, root_dir: Optional[str] = None):
        if root_dir is None:
            root_dir = "."
        if root_dir:
            os.makedirs(root_dir, exist_ok=True)
        self._root_dir = root_dir
        self._investigations = os.path.join(root_dir, "investigations.json")

    def start_investigation(self, investigation: dict) -> None:
        investigation["instrument"] = {"name": investigation["instrument"]}
        _add_table(self._investigations, investigation)

    def store_dataset(self, dataset: dict) -> None:
        investigation = _find_data(self._investigations, dataset["startDate"])
        if investigation is None:
            logger.error(
                "Dataset not stored because no investigation found: %s", dataset
            )
            return
        filename = os.path.join(self._root_dir, f"datasets{investigation['id']}.json")
        _add_table(filename, dataset)

    def get_investigations(self, instrument: str, experiment: str) -> List[Dict]:
        return [
            investigation
            for investigation in _read_table(self._investigations)
            if experiment == investigation["experiment"]
            and instrument == investigation["instrument"]["name"]
        ]

    def get_datasets(self, investigation_id) -> List[Dict]:
        filename = os.path.join(self._root_dir, f"datasets{investigation_id}.json")
        return _read_table(filename)


def _read_table(filename: str) -> List[dict]:
    if not os.path.isfile(filename):
        return list()
    with open(filename, "r") as f:
        return json.load(f)


def _update_table(filename: str, data: dict) -> Dict:
    with open(filename, "w") as f:
        json.dump(data, f)
    logger.info("Metadata in %s updated", filename)


def _add_table(filename: str, data: dict) -> int:
    table = _read_table(filename)
    if table:
        data_id = max(row["id"] for row in table) + 1
    else:
        data_id = 0
    data = dict(data)
    data["id"] = data_id
    table.append(data)
    logger.info("Add metadata to %s: %s", filename, data)
    _update_table(filename, table)
    return data_id


def _find_data(filename: str, date: str) -> Optional[Dict]:
    date = datetime.fromisoformat(date).astimezone()
    for data in _read_table(filename):
        start_date = datetime.fromisoformat(data["startDate"]).astimezone()
        end_date = data.get("endDate")
        if end_date is None:
            # infinite timeslot
            inside_timeslot = date >= start_date
        else:
            # finite timeslot
            end_date = datetime.fromisoformat(end_date).astimezone()
            inside_timeslot = date >= start_date and date <= end_date
        if inside_timeslot:
            return data
