from dataclasses import dataclass
from datetime import datetime


@dataclass
class Header:
    full_header: str = ""

    program_id: str | None = None
    app_lotw_lastqsl: datetime | None = None
    app_lotw_numrec: int | None = None

    def __repr__(self) -> str:
        return f"Header(program_id='{self.program_id}', app_lotw_lastqsl={self.app_lotw_lastqsl}, app_lotw_numrec={self.app_lotw_numrec})"
