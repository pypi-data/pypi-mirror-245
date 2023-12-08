import re
from io import TextIOWrapper
from pathlib import Path
from typing import IO

from ..dataclasses import Header, QSOReport
from ..logger import setup_logger
from .match_header_tag import match_header_tag
from .match_report_tag import match_report_tag

logger = setup_logger()

EOH_MATCH = re.compile(r"<eoh>")
EOR_MATCH = re.compile(r"<eor>")

# Group 1 is tag, group 2 is length, group 3 is value
TAG_MATCH = re.compile(r"^<(.*):(\d*)>(.*)$")


def parse_adi(
    file: str | Path | TextIOWrapper | IO[bytes],
    encoding="utf-8",
    errors="replace",
) -> tuple[Header, list[QSOReport]]:
    if isinstance(file, TextIOWrapper):
        return main_loop(adif_file=file)

    elif not isinstance(file, (str, Path)):
        file = TextIOWrapper(buffer=file, encoding=encoding, errors=errors)
        return main_loop(adif_file=file)

    else:
        with open(
            file=file,
            mode="r",
            encoding=encoding,
            errors=errors,
        ) as adif_file:
            return main_loop(adif_file=adif_file)


def main_loop(adif_file: TextIOWrapper) -> tuple[Header, list[QSOReport]]:
    header = Header()
    qso_reports: list[QSOReport] = []

    # Get Header
    while True:
        current_line: str = adif_file.readline()

        # If eof
        if not current_line:
            break

        header.full_header += current_line

        tag_match = re.match(pattern=TAG_MATCH, string=current_line)

        if tag_match:
            tag_str, _, value = tag_match.groups()

            match_header_tag(
                header=header,
                tag_str=tag_str,
                value=value,
            )

        if re.match(pattern=EOH_MATCH, string=current_line):
            break

    # Get Reports
    while True:
        qso_report = QSOReport()

        while True:
            current_line: str = adif_file.readline()

            # If eof
            if not current_line:
                break

            qso_report.full_report += current_line

            tag_match = re.match(pattern=TAG_MATCH, string=current_line)

            if tag_match:
                tag_str, _, value = tag_match.groups()

                match_report_tag(
                    qso_report=qso_report,
                    tag_str=tag_str,
                    value=value,
                )

            if re.match(pattern=EOR_MATCH, string=current_line):
                qso_reports.append(qso_report)
                break

        # If eof
        if not current_line:
            break

    return header, qso_reports
