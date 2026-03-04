import logging
import sys


def init_logger() -> None:
    logging.basicConfig(
        stream=sys.stdout,
        datefmt="%Y-%m-%d %H:%M:%S",
        format="[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s",
        style="%",
        level=logging.INFO,
        encoding="utf-8",
        force=True,
    )
