from dataclasses import dataclass
from datetime import datetime

from ..logger import logger


@dataclass
class Header:
    full_header: str = ""

    program_id: str | None = None
    app_lotw_numrec: int | None = None
    app_lotw_lastqsl: datetime | None = None

    def __repr__(self) -> str:
        return f"Header(program_id='{self.program_id}', app_lotw_lastqsl={self.app_lotw_lastqsl}, app_lotw_numrec={self.app_lotw_numrec})"

    def assign_tag(
        self,
        tag: str,
        value: str,
    ) -> bool:
        match tag:
            case "PROGRAMID":
                self.program_id = value
            case "APP_LoTW_LASTQSL":
                self.app_lotw_lastqsl = datetime.strptime(
                    value,
                    "%Y-%m-%d %H:%M:%S",
                )
            case "APP_LoTW_NUMREC":
                self.app_lotw_numrec = int(value)
            case _:
                logger.warn(f"Unknown tag: {tag}, {value}")
                return False
        return True
