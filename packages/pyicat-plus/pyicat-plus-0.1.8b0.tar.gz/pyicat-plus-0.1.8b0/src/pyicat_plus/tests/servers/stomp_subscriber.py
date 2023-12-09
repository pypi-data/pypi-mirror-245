import stomp
import json
import socket
import logging
import threading
from enum import Enum
from typing import Optional
from json.decoder import JSONDecodeError

import xmltodict
from xml.parsers.expat import ExpatError

from pyicat_plus.tests.servers.utils import basic_config
from pyicat_plus.tests.servers.icat_db import IcatDb

logger = logging.getLogger("STOMP SUBSCRIBER")
basic_config(
    logger=logger,
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

MessageType = Enum("MessageType", "investigation dataset archiving unknown")


class MyListener(stomp.ConnectionListener):
    def __init__(self, conn, icat_data_dir: Optional[str] = None):
        self.conn = conn
        self.s_out = None
        self.icatdb = IcatDb(icat_data_dir)
        super().__init__()

    def redirect_messages(self, port):
        if self.s_out is not None:
            self.s_out.close()
        self.s_out = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s_out.connect(("localhost", port))
        logger.info(f"Redirect received messages to port {port}")

    def on_message(self, frame):
        message = frame.body
        logger.info(f"received message:\n {message}")

        message_type = None
        try:
            message = xmltodict.parse(
                message,
                process_namespaces=True,
                namespaces={"http://www.esrf.fr/icat": None},
            )
        except ExpatError:
            try:
                message = json.loads(message)
            except JSONDecodeError:
                message_type = MessageType.unknown
            else:
                message_type = MessageType.archiving
        else:
            if "investigation" in message:
                message_type = MessageType.investigation
            elif "dataset" in message:
                message_type = MessageType.dataset

        # Only access specific destinations
        header = frame.headers
        if header.get("destination") not in [
            "/queue/icatIngest",
            "/queue/icatArchiveRestoreStatus",
        ]:
            return

        # Only accept valid proposals
        if message_type in (message_type.investigation, message_type.dataset):
            if message_type is message_type.investigation:
                data = message["investigation"]
                proposal = data["experiment"]
            else:
                data = message["dataset"]
                proposal = data["investigation"]
            if "666" in proposal:
                logger.info(
                    "Do not register %s for invalid proposal '%s'",
                    message_type,
                    proposal,
                )
                return

        # Store data
        if message_type in (message_type.investigation, message_type.dataset):
            if message_type is message_type.investigation:
                self.icatdb.start_investigation(data)
            else:
                self.icatdb.store_dataset(data)

        # Notify that data is valid
        if self.s_out is not None:
            self.s_out.sendall(frame.body.encode() + b"\n")


def main(
    host=None, port=60001, queue=None, port_out=0, icat_data_dir: Optional[str] = None
):
    if not host:
        host = "localhost"
    if not queue:
        queue = "/queue/icatIngest"
    conn = stomp.Connection([(host, port)])
    # Listener will run in a different thread
    listener = MyListener(conn, icat_data_dir)
    conn.set_listener("", listener)
    conn.connect("guest", "guest", wait=True)
    conn.subscribe(destination=queue, id=1, ack="auto")
    logger.info(f"subscribed to {queue} on STOMP {host}:{port}")
    if port_out:
        listener.redirect_messages(port_out)
        listener.s_out.sendall(b"LISTENING\n")
    logger.info("CTRL-C to stop")
    try:
        threading.Event().wait()
    finally:
        logger.info("Exit.")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="STOMP client which subscribes to a STOMP queue and redirect its output to a socket"
    )
    parser.add_argument(
        "--host", default="localhost", type=str, help="STOMP server host"
    )
    parser.add_argument("--port", default=60001, type=int, help="STOMP server port")
    parser.add_argument(
        "--queue", default="/queue/icatIngest", type=str, help="STOMP queue"
    )
    parser.add_argument("--port_out", default=0, type=int, help="output socket")
    parser.add_argument(
        "--icat_data_dir", default=None, type=str, help="Dataset directory"
    )
    args = parser.parse_args()

    main(
        host=args.host,
        port=args.port,
        port_out=args.port_out,
        queue=args.queue,
        icat_data_dir=args.icat_data_dir,
    )
