import os
import sys
import argparse
import datetime
from time import sleep
from glob import glob
from typing import Optional, Dict, Any, List, Tuple

import h5py
from ..client.main import IcatClient
from ..client.bliss import get_icat_client


def sync_raw(
    icat_client: IcatClient,
    beamline: Optional[str] = None,
    proposal: Optional[str] = None,
    session: Optional[str] = None,
    root_dir: Optional[str] = None,
    dry_run: bool = True,
    raw_data_format: str = "esrfv3",
):
    if beamline is None:
        beamline = "*"
    if proposal is None:
        proposal = "*"
    if session is None:
        session = "*"
    session_filter = _get_session_dir(
        proposal, beamline, session, root_dir=root_dir, raw_data_format=raw_data_format
    )
    for session_dir in glob(session_filter):
        proposal2, beamline2, session2 = session_dir.split(os.sep)[-3:]
        if not session2.isdigit():
            continue
        session = os.path.basename(session_dir)
        sync_session(
            icat_client,
            proposal2,
            beamline2,
            session2,
            dry_run=dry_run,
            raw_data_format=raw_data_format,
        )


def sync_session(
    icat_client: IcatClient,
    proposal: str,
    beamline: str,
    session: str,
    root_dir: Optional[str] = None,
    dry_run: bool = True,
    allow_open_ended: bool = True,
    raw_data_format: str = "esrfv3",
) -> None:
    info = _raw_vs_icat_info(
        icat_client,
        proposal,
        beamline,
        session,
        root_dir=root_dir,
        raw_data_format=raw_data_format,
        allow_open_ended=allow_open_ended,
    )

    # Print raw info
    raw = info.get("raw")
    if raw is None:
        return
    separator = "\n--------------------------------"
    print(separator)
    print("Directory:", raw["root_dir"])
    print(" Start time:", raw["startdate"])

    # Print ICAT info
    print("")
    icat = info.get("icat")
    if icat is None:
        print("No corresponding investigation")
        return
    print("Investigation ID:", icat["id"])
    print(" URL:", icat["url"])
    if "startdate" not in icat:
        print("Invalid investigation (no start date)")
        print(separator)
        return
    print(" Start time:", icat["startdate"])
    if "enddate" not in icat:
        print("Open-ended investigation (not official)")
        print(separator)
    else:
        print(" End time:", icat["enddate"])

    # Print dataset info
    invalid = info["datasets"]["invalid"]
    if invalid:
        print("")
        print("Invalid datasets:")
        for dataset in invalid:
            print(" ", dataset["store_kwargs"]["path"])
            if dataset["print_info"]:
                print("   " + "\n   ".join(dataset["print_info"]))

    registered = info["datasets"]["registered"]
    if registered:
        print("")
        print("Registered datasets:")
        for dataset in registered:
            print(" ", dataset["store_kwargs"]["path"])
            if dataset["print_info"]:
                print("   " + "\n   ".join(dataset["print_info"]))

    unregistered = info["datasets"]["unregistered"]
    if unregistered:
        print("")
        print("Unregistered datasets:")
        for dataset in unregistered:
            print(" ", dataset["store_kwargs"]["path"])
            if dataset["print_info"]:
                print("   " + "\n   ".join(dataset["print_info"]))

    notuploaded = info["datasets"]["notuploaded"]
    if notuploaded:
        print("")
        print("Datasets not uploaded:")
        for dataset in notuploaded:
            print(" ", dataset["store_kwargs"]["path"])
            if dataset["print_info"]:
                print("   " + "\n   ".join(dataset["print_info"]))

    print("")
    if invalid or notuploaded or unregistered:
        print("Datasets (TODO):")
    elif not registered:
        print("Datasets (EMPTY):")
    else:
        print("Datasets (DONE):")
    print(f" {len(registered)} registered")
    print(f" {len(invalid)} invalid")
    print(f" {len(notuploaded)} not uploaded")
    print(f" {len(unregistered)} unregistered")
    print(separator)

    # Allow the user to cancel
    if unregistered and not dry_run:
        result = input("Register datasets with ICAT? (y/[n])")
        if result not in ("y", "yes"):
            return

    # Register datasets that failed to be registered
    for dataset in notuploaded:
        kwargs = dataset["store_kwargs"]
        metadata_file = dataset["metadata_file"]
        print("-> Upload dataset:", kwargs["path"])
        print("    Name:", kwargs["dataset"])
        print("    Sample:", kwargs["metadata"]["Sample_name"])
        dataset_startdate = kwargs["metadata"]["startDate"]
        dataset_enddate = kwargs["metadata"]["endDate"]
        print("    Start time:", dataset_startdate)
        print("    End time:", dataset_enddate)
        print("    Duration:", dataset_enddate - dataset_startdate)
        if not dry_run:
            icat_client.store_dataset_from_file(metadata_file)
            sleep(1)

    # Register datasets that were not even attempted to be registered
    for dataset in unregistered:
        kwargs = dataset["store_kwargs"]
        print("-> Register dataset:", kwargs["path"])
        print("    Name:", kwargs["dataset"])
        print("    Sample:", kwargs["metadata"]["Sample_name"])
        dataset_startdate = kwargs["metadata"]["startDate"]
        dataset_enddate = kwargs["metadata"]["endDate"]
        print("    Start time:", dataset_startdate)
        print("    End time:", dataset_enddate)
        print("    Duration:", dataset_enddate - dataset_startdate)
        if not dry_run:
            icat_client.store_dataset(**kwargs)
            sleep(1)


def _raw_vs_icat_info(
    icat_client: IcatClient,
    proposal: str,
    beamline: str,
    session: str,
    root_dir: Optional[str] = None,
    raw_data_format: str = "esrfv3",
    allow_open_ended: bool = True,
) -> Optional[List[Dict]]:
    info = dict()

    # Raw data directory with session start time
    raw_root_dir = _get_raw_data_dir(
        proposal, beamline, session, root_dir=root_dir, raw_data_format=raw_data_format
    )

    try:
        session_startdate_fromdir = datetime.datetime.combine(
            datetime.datetime.strptime(session, "%Y%m%d").date(),
            datetime.time(hour=8),  # sessions start at 8 a.m.
        ).astimezone()
    except ValueError:
        return info

    info["raw"] = {"root_dir": raw_root_dir, "startdate": session_startdate_fromdir}

    # Get the ICAT investigation related to the raw data directory
    investigation = icat_client.investigation_info(
        beamline,
        proposal,
        date=session_startdate_fromdir,
        allow_open_ended=allow_open_ended,
    )
    if not investigation:
        return info
    info["icat"] = {"id": investigation["id"], "url": investigation["data portal"]}
    if "startDate" not in investigation:
        return info
    session_startdate = datetime.datetime.fromisoformat(
        investigation["startDate"]
    ).astimezone()
    info["icat"]["startdate"] = session_startdate
    if investigation.get("endDate"):
        session_enddate = datetime.datetime.fromisoformat(
            investigation["endDate"]
        ).astimezone()
        info["icat"]["enddate"] = session_enddate
    else:
        session_enddate = None

    # Get all ddatasets from the raw data and compare with
    # the datasets registered with the ICAT investigation
    unregistered = list()
    notuploaded = list()
    registered = list()
    invalid = list()
    info["datasets"] = {
        "unregistered": unregistered,
        "notuploaded": notuploaded,
        "registered": registered,
        "invalid": invalid,
    }

    registered_dataset_dirs = {
        dset.path
        for dset in icat_client.registered_dataset_ids(
            beamline,
            proposal,
            date=session_startdate_fromdir,
            allow_open_ended=allow_open_ended,
        )
    }

    dataset_filter = _get_dataset_filter(raw_root_dir, raw_data_format=raw_data_format)
    metadata_root = os.path.join(raw_root_dir, "__icat__")
    for dataset_dir in glob(dataset_filter):
        if not os.path.isdir(dataset_dir):
            continue
        store_kwargs = {"path": dataset_dir, "proposal": proposal, "beamline": beamline}
        print_info = list()
        metadata_file = os.path.join(
            metadata_root, os.path.basename(dataset_dir) + ".xml"
        )
        dataset = {
            "store_kwargs": store_kwargs,
            "print_info": print_info,
            "metadata_file": metadata_file,
        }

        dataset_name = _raw_dataset_name(dataset_dir, raw_data_format=raw_data_format)
        if not dataset_name:
            invalid.append(dataset)
            continue
        store_kwargs["dataset"] = dataset_name

        if dataset_dir in registered_dataset_dirs:
            registered.append(dataset)
            continue

        dataset_metadata, pinfo = _raw_dataset_info(
            dataset_dir,
            session_startdate,
            session_enddate,
            raw_data_format=raw_data_format,
        )
        print_info.extend(pinfo)
        if dataset_metadata is None:
            invalid.append(dataset)
            continue

        store_kwargs["metadata"] = dataset_metadata
        if os.path.exists(metadata_file):
            notuploaded.append(dataset)
        else:
            unregistered.append(dataset)

    return info


def _get_raw_data_dir(
    proposal: str,
    beamline: str,
    session: str,
    root_dir: Optional[str] = None,
    raw_data_format: str = "esrfv3",
) -> str:
    session_dir = _get_session_dir(
        proposal, beamline, session, root_dir=root_dir, raw_data_format=raw_data_format
    )
    if raw_data_format in ("esrfv3", "id16bspec"):
        return os.path.join(session_dir, "RAW_DATA")
    if raw_data_format == "esrfv2":
        return os.path.join(session_dir, "raw")
    if raw_data_format == "esrfv1":
        return session_dir
    raise NotImplementedError(f"Raw data format '{raw_data_format}' is not supported")


def _get_session_dir(
    proposal: str,
    beamline: str,
    session: str,
    root_dir: Optional[str] = None,
    raw_data_format: str = "esrfv3",
) -> str:
    if raw_data_format in ("esrfv1", "esrfv2", "esrfv3", "id16bspec"):
        if root_dir is None:
            root_dir = os.path.join(os.sep, "data", "visitor")
        return os.path.join(root_dir, proposal, beamline, session)
    raise NotImplementedError(f"Raw data format '{raw_data_format}' is not supported")


def _get_dataset_filter(raw_root_dir: str, raw_data_format: str = "esrfv3") -> str:
    if raw_data_format in ("esrfv1", "esrfv2", "esrfv3", "id16bspec"):
        return os.path.join(raw_root_dir, "*", "*")
    raise NotImplementedError(f"Raw data format '{raw_data_format}' is not supported")


def _raw_dataset_name(
    dataset_dir: str, raw_data_format: str = "esrfv3"
) -> Optional[str]:
    if raw_data_format in ("esrfv1", "esrfv2", "esrfv3"):
        collection, collection_dataset = dataset_dir.split(os.sep)[-2:]
        if not collection_dataset.startswith(collection):
            return None
        return collection_dataset[len(collection) + 1 :]
    elif raw_data_format == "id16bspec":
        return dataset_dir.split(os.sep)[-1]
    raise NotImplementedError(f"Raw data format '{raw_data_format}' is not supported")


def _raw_dataset_info(
    dataset_dir: str,
    session_startdate: datetime.datetime,
    session_enddate: Optional[datetime.datetime],
    raw_data_format: str = "esrfv3",
) -> Tuple[Optional[Dict[str, str]], List[str]]:
    """Returns `None` when the directory is not a raw Bliss dataset. Returns dataset metadata otherwise."""
    pinfo = list()
    if raw_data_format in ("esrfv1", "esrfv2", "esrfv3"):
        dataset_metadata = _raw_dataset_info_esrf(dataset_dir)
    elif raw_data_format == "id16bspec":
        dataset_metadata = _raw_dataset_info_id16bspec(dataset_dir)
    else:
        pinfo.append(f"Raw data format '{raw_data_format}' is not supported")

    if set(dataset_metadata) != {"Sample_name", "startDate", "endDate"}:
        pinfo.append(
            f"Cannot extract dataset metadata (assuming format={raw_data_format})"
        )
        return None, pinfo

    dataset_startdate, msg = _force_date_within_range(
        session_startdate,
        session_enddate,
        datetime.datetime.fromisoformat(dataset_metadata["startDate"]).astimezone(),
        end=False,
    )
    if msg:
        pinfo.append(msg)
    dataset_enddate, msg = _force_date_within_range(
        session_startdate,
        session_enddate,
        datetime.datetime.fromisoformat(dataset_metadata["endDate"]).astimezone(),
        end=True,
    )
    if msg:
        pinfo.append(msg)
    dataset_metadata["startDate"] = dataset_startdate
    dataset_metadata["endDate"] = dataset_enddate

    return dataset_metadata, pinfo


def _raw_dataset_info_esrf(dataset_dir: str) -> Dict[str, str]:
    dataset_metadata = dict()

    dataset_file = os.path.join(dataset_dir, f"{os.path.basename(dataset_dir)}.h5")
    if not os.path.exists(dataset_file):
        return dataset_metadata

    enddate = None
    with h5py.File(dataset_file, "r", locking=False) as f:
        if not _is_bliss_raw_dataset_file(f):
            return dataset_metadata
        startdate = f.attrs.get("file_time")
        for scan in map(str, sorted(map(float, list(f)))):
            sample_name = _read_hdf5_dataset(f, f"/{scan}/sample/name", default=None)
            if sample_name is not None:
                dataset_metadata["Sample_name"] = sample_name
            enddate = _read_hdf5_dataset(f, f"/{scan}/end_time", default=enddate)

    if startdate is not None:
        dataset_metadata["startDate"] = startdate
    if enddate is not None:
        dataset_metadata["endDate"] = enddate

    return dataset_metadata


def _raw_dataset_info_id16bspec(dataset_dir: str) -> Dict[str, str]:
    dataset_metadata = dict()

    proposal, _, _, _, sample_name, dataset = dataset_dir.split(os.sep)[-6:]
    filename = f"{proposal}-{sample_name}-{dataset}.h5"
    dataset_file = os.path.join(dataset_dir, filename)

    if not os.path.exists(dataset_file):
        return dataset_metadata

    startdate = None
    enddate = None
    with h5py.File(dataset_file, "r", locking=False) as f:
        for name in f:
            entry = f[name]
            try:
                startdate = _read_hdf5_dataset(entry, "start_time", default=None)
                enddate = _read_hdf5_dataset(entry, "end_time", default=None)
            except KeyError:
                return dataset_metadata
            break

    if startdate is not None:
        dataset_metadata["startDate"] = startdate
    if enddate is not None:
        dataset_metadata["endDate"] = enddate
    dataset_metadata["Sample_name"] = sample_name
    return dataset_metadata


def _is_bliss_raw_dataset_file(f: h5py.File) -> bool:
    return f.attrs.get("creator", "").lower() == "bliss"


def _read_hdf5_dataset(parent: h5py.Group, name: str, default=None) -> Any:
    try:
        value = parent[name][()]
    except KeyError:
        return default
    try:
        return value.decode()
    except AttributeError:
        pass
    return value


def _force_date_within_range(
    session_startdate: datetime.datetime,
    session_enddate: Optional[datetime.datetime],
    dataset_date: datetime.datetime,
    end: bool = False,
) -> Tuple[datetime.datetime, Optional[str]]:
    if end:
        action = "ended"
        dstart_seconds = 2
        dend_seconds = 1
    else:
        action = "started"
        dstart_seconds = 1
        dend_seconds = 2
    msg = None
    if session_enddate is not None and dataset_date >= session_enddate:
        msg = f"{action} {dataset_date-session_enddate} after the end of the session"
        dataset_date = session_enddate - datetime.timedelta(seconds=dend_seconds)
    if dataset_date <= session_startdate:
        msg = (
            f"{action} {session_startdate-dataset_date} before the start of the session"
        )
        dataset_date = session_startdate + datetime.timedelta(seconds=dstart_seconds)
    return dataset_date, msg


def main(argv=None):
    if argv is None:
        argv = sys.argv

    parser = argparse.ArgumentParser(
        description="Register missing raw dataset with ICAT"
    )
    parser.add_argument("--beamline", required=False, help="Beamline name (e.g. id00)")
    parser.add_argument(
        "--proposal", required=False, help="Proposal name (e.g. ihch123)"
    )
    parser.add_argument(
        "--session", required=False, help="Session name (e.g. 20231028)"
    )
    parser.add_argument(
        "--register",
        action="store_true",
        required=False,
        help="Register dataset with ICAT when needed",
    )
    parser.add_argument(
        "--format",
        required=False,
        choices=["esrfv1", "esrfv2", "esrfv3", "id16bspec"],
        default="esrfv3",
        help="Raw data structure",
    )
    args = parser.parse_args(argv[1:])

    icat_client = get_icat_client(timeout=100)

    sync_raw(
        icat_client,
        beamline=args.beamline,
        proposal=args.proposal,
        session=args.session,
        dry_run=not args.register,
        raw_data_format=args.format,
    )


if __name__ == "__main__":
    sys.exit(main())
