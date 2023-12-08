from datetime import datetime

from ..dataclasses import Header
from ..logger import setup_logger

logger = setup_logger()


def match_header_tag(header: Header, tag_str: str, value: str) -> None:
    match tag_str:
        case "PROGRAMID":
            header.program_id = value
        case "APP_LoTW_LASTQSL":
            header.app_lotw_lastqsl = datetime.strptime(
                value,
                "%Y-%m-%d %H:%M:%S",
            )
        case "APP_LoTW_NUMREC":
            header.app_lotw_numrec = int(value)
        case _:
            logger.warn(f"Unknown tag: {tag_str}, {value}")
