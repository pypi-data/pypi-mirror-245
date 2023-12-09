import os
from datetime import datetime, timedelta
from typing import Generator
from contextlib import contextmanager

import h5py

from ..apps import sync_raw
from ..client.main import IcatClient


def test_unregistered_datasets(tmpdir, icat_main_client):
    client, messages = icat_main_client

    root_dir = str(tmpdir)
    beamline = "id99"
    proposal = "hg333"

    startdate = datetime.fromisoformat("2023-10-19T08:00:00+02:00")
    enddate = startdate + timedelta(days=5)
    _generate_esrf_experiment(client, root_dir, proposal, beamline, startdate, enddate)
    messages.get(timeout=10)

    args = client, "hg333", "id99", "20231019"
    kwargs = {"root_dir": root_dir, "raw_data_format": "esrfv3"}

    info = sync_raw._raw_vs_icat_info(*args, **kwargs)
    assert len(info["datasets"]["registered"]) == 0
    assert len(info["datasets"]["unregistered"]) == 6

    for dataset in info["datasets"]["unregistered"][:3]:
        client.store_dataset(**dataset["store_kwargs"])
        messages.get(timeout=10)

    info = sync_raw._raw_vs_icat_info(*args, **kwargs)
    assert len(info["datasets"]["registered"]) == 3
    assert len(info["datasets"]["unregistered"]) == 3

    for dataset in info["datasets"]["unregistered"][:3]:
        client.store_dataset(**dataset["store_kwargs"])
        messages.get(timeout=10)

    info = sync_raw._raw_vs_icat_info(*args, **kwargs)
    assert len(info["datasets"]["registered"]) == 6
    assert len(info["datasets"]["unregistered"]) == 0


def test_unregistered_datasets_content(tmpdir, icat_main_client):
    client, messages = icat_main_client

    root_dir = str(tmpdir)
    beamline = "id99"
    proposal = "hg333"

    startdate = datetime.fromisoformat("2023-10-19T08:00:00+02:00")
    enddate = startdate + timedelta(days=5)
    _generate_esrf_experiment(client, root_dir, proposal, beamline, startdate, enddate)
    messages.get(timeout=10)

    info = sync_raw._raw_vs_icat_info(
        client, "hg333", "id99", "20231019", root_dir=root_dir, raw_data_format="esrfv3"
    )
    unregistered = [adict["store_kwargs"] for adict in info["datasets"]["unregistered"]]
    unregistered = sorted(unregistered, key=lambda adict: adict["path"])

    tz = startdate.tzinfo
    for dataset in unregistered:
        metadata = dataset["metadata"]
        metadata["startDate"] = metadata["startDate"].astimezone(tz=tz).isoformat()
        metadata["endDate"] = metadata["endDate"].astimezone(tz=tz).isoformat()
        dataset["path"] = os.path.relpath(dataset["path"], root_dir)

    expected = [
        {
            "beamline": "id99",
            "dataset": "0001",
            "metadata": {
                "Sample_name": "sample0",
                "endDate": "2023-10-20T04:00:00+02:00",
                "startDate": "2023-10-19T08:00:01+02:00",
            },
            "path": "hg333/id99/20231019/RAW_DATA/collection0/collection0_0001",
            "proposal": "hg333",
        },
        {
            "beamline": "id99",
            "dataset": "0001",
            "metadata": {
                "Sample_name": "sample1",
                "endDate": "2023-10-21T00:00:00+02:00",
                "startDate": "2023-10-19T08:00:01+02:00",
            },
            "path": "hg333/id99/20231019/RAW_DATA/collection1/collection1_0001",
            "proposal": "hg333",
        },
        {
            "beamline": "id99",
            "dataset": "0002",
            "metadata": {
                "Sample_name": "sample1",
                "endDate": "2023-10-22T16:00:00+02:00",
                "startDate": "2023-10-21T00:00:00+02:00",
            },
            "path": "hg333/id99/20231019/RAW_DATA/collection1/collection1_0002",
            "proposal": "hg333",
        },
        {
            "beamline": "id99",
            "dataset": "0001",
            "metadata": {
                "Sample_name": "sample3",
                "endDate": "2023-10-24T07:59:59+02:00",
                "startDate": "2023-10-24T07:59:58+02:00",
            },
            "path": "hg333/id99/20231019/RAW_DATA/collection3/collection3_0001",
            "proposal": "hg333",
        },
        {
            "beamline": "id99",
            "dataset": "0002",
            "metadata": {
                "Sample_name": "sample3",
                "endDate": "2023-10-24T07:59:59+02:00",
                "startDate": "2023-10-24T07:59:58+02:00",
            },
            "path": "hg333/id99/20231019/RAW_DATA/collection3/collection3_0002",
            "proposal": "hg333",
        },
        {
            "beamline": "id99",
            "dataset": "0001",
            "metadata": {
                "Sample_name": "sample4",
                "endDate": "2023-10-24T07:59:59+02:00",
                "startDate": "2023-10-23T12:00:00+02:00",
            },
            "path": "hg333/id99/20231019/RAW_DATA/collection4/collection4_0001",
            "proposal": "hg333",
        },
    ]

    assert unregistered == expected


def _generate_esrf_experiment(
    client: IcatClient,
    root_dir: str,
    proposal: str,
    beamline: str,
    startdate: datetime,
    enddate: datetime,
):
    session = startdate.strftime("%Y%m%d")
    raw_root_dir = os.path.join(root_dir, proposal, beamline, session, "RAW_DATA")
    os.makedirs(raw_root_dir, exist_ok=True)

    client.start_investigation(
        beamline=beamline,
        proposal=proposal,
        start_datetime=startdate,
        end_datetime=enddate,
    )

    ndatasets = 5
    dataset_duration, deadtime = _chunk_duration(startdate, enddate, ndatasets)

    now = startdate - dataset_duration / 2
    _normal_dataset_file(
        raw_root_dir, "collection0", "0001", "sample0", now, dataset_duration
    )

    now = startdate + deadtime
    _normal_dataset_file(
        raw_root_dir, "collection1", "0001", "sample1", now, dataset_duration
    )

    now += dataset_duration + deadtime
    _normal_dataset_file(
        raw_root_dir, "collection1", "0002", "sample1", now, dataset_duration
    )

    now += dataset_duration + deadtime
    _empty_dataset_file(
        raw_root_dir, "collection2", "0001", "sample2", now, dataset_duration
    )

    now += dataset_duration + deadtime
    _normal_dataset_file(
        raw_root_dir, "collection3", "0001", "sample3", now, dataset_duration
    )

    now += dataset_duration + deadtime
    _normal_dataset_file(
        raw_root_dir, "collection3", "0002", "sample3", now, dataset_duration
    )

    now = enddate - dataset_duration / 2
    _normal_dataset_file(
        raw_root_dir, "collection4", "0001", "sample4", now, dataset_duration
    )


def _chunk_duration(
    starttime: datetime,
    endtime: datetime,
    nchunks: int,
    deadtime: int = 0,
):
    deadtime = timedelta(seconds=deadtime)
    return (endtime - starttime - (nchunks + 1) * deadtime) / 3, deadtime


def _normal_dataset_file(
    raw_root_dir: str,
    collection: str,
    dataset: str,
    sample_name: str,
    starttime: datetime,
    duration: timedelta,
) -> None:
    with _dataset_file(raw_root_dir, collection, dataset, sample_name) as f:
        f.attrs["creator"] = "Bliss"
        f.attrs["file_time"] = starttime.isoformat()

        nscans = 3
        scan_duration, deadtime = _chunk_duration(
            starttime, starttime + duration, nscans
        )

        now = starttime + deadtime
        _save_scan(f, now, scan_duration, sample_name)

        now += scan_duration + deadtime
        _save_scan(f, now, scan_duration, sample_name, failed=True)

        now += scan_duration + deadtime
        _save_scan(f, now, scan_duration, sample_name)


def _empty_dataset_file(
    raw_root_dir: str,
    collection: str,
    dataset: str,
    sample_name: str,
    starttime: datetime,
    duration: timedelta,
) -> None:
    with _dataset_file(raw_root_dir, collection, dataset, sample_name):
        pass


def _save_scan(
    f: h5py.File,
    starttime: datetime,
    duration: timedelta,
    sample_name: str,
    failed: bool = False,
) -> None:
    scans = list(f)
    if scans:
        scan = max(map(int, map(float, scans))) + 1
    else:
        scan = 1
    name = f"{scan}.1"
    grp = f.create_group(name)
    grp["start_time"] = starttime.isoformat()
    if failed:
        return
    grp["end_time"] = (starttime + duration).isoformat()
    grp["sample/name"] = sample_name


@contextmanager
def _dataset_file(
    raw_root_dir: str, collection: str, dataset: str, sample_name: str
) -> Generator[h5py.File, None, None]:
    basename = f"{collection}_{dataset}"
    filename = basename + ".h5"
    dataset_dir = os.path.join(raw_root_dir, collection, basename)
    os.makedirs(dataset_dir, exist_ok=True)
    with h5py.File(os.path.join(dataset_dir, filename), mode="w") as f:
        yield f
