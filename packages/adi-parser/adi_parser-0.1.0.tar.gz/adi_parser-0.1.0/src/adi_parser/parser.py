import re
from io import TextIOWrapper
from pathlib import Path
from typing import IO, Any

from .dataclasses import Header, QSOReport

type TupleOrDict = tuple[Header, list[QSOReport]] | dict[str, Any]

HEADER_MATCH = re.compile(r"(.*)<eoh>", flags=re.S)
RECORD_MATCH = re.compile(r"\n*(.*?)<eor>", flags=re.S)

# tag, length, type, value opt 1, comment, value opt 2
# 1    2       3     4            5        6
TAG_MATCH = re.compile(
    r"<([^>:]+)(?::([^>:]+))?(?::([^>:]+))?>(?:(?:([^<\n]*?)(?:\b\s*//\s*(?:\b\n)*)([^<\n]*))|([^<\n]*))"
)


def parse_adi(
    file: str | Path | TextIOWrapper | IO[bytes],
    encoding="utf-8",
    errors="replace",
    return_type: TupleOrDict = tuple[Header, list[QSOReport]],
) -> TupleOrDict:
    """Parses a .adi file, by default returns a tuple of the Header and a list of
    QSO Reports in their dataclass form.

    Headers and QSO Reports are designed for LoTW data. If your .adi is not from
    LoTW, its suggested to use `return_type = dict` to get all fields, regardless
    of their origin.

    The dict return structure:
    ```py
    result = {
        "header": {
            "full_text": str,
            "argument_1": str,
            "argument_2": str,
            ...
        },
        "qso_reports": [
            {
                "full_text": str,
                "argument_1": {
                    "value": str,
                    "length": int,
                    "type": str | None,
                    "comment": str | None,
                },
                "argument_2": {
                    ...
                },
                ...
            },
            ...
        ]
    }
    ```

    Args:
        file (str | Path | TextIOWrapper | IO[bytes]): The file to read from, either as a path or as most .read()-able objects.
        encoding (str, optional): The encoding of the file. Defaults to "utf-8".
        errors (str, optional): The method of encoding error handling. Defaults to "replace".
        return_type (TupleOrDict, optional): What to return as. Defaults to tuple[Header, list[QSOReport]].

    Returns:
        TupleOrDict: Either a tuple of Header and list[QSOReport], or a dict of all values.
    """

    if return_type == dict:
        main_loop = main_loop_dict
    else:
        main_loop = main_loop_tuple

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


def main_loop_dict(adif_file: TextIOWrapper) -> dict[str, Any]:
    header: dict[str, Any] = {}
    qso_reports: list[dict[str, Any]] = []

    text = adif_file.read()

    header_match = re.match(HEADER_MATCH, text)
    header.update({"full_text": header_match.group(1)})

    header_matches = re.findall(
        pattern=TAG_MATCH,
        string=header.get("full_text"),
    )

    for match in header_matches:
        tag, _, _, value_opt_1, _, value_opt_2 = match

        header.update({tag: value_opt_1 or value_opt_2})

    records = re.findall(RECORD_MATCH, text[header_match.end(0) :])
    for record in records:
        qso_report: dict[str, Any] = {}
        qso_report.update({"full_text": record})

        matches = re.findall(pattern=TAG_MATCH, string=record)

        for match in matches:
            qso_report.update(
                {
                    match[0]: {
                        "value": match[3] or match[5],
                        "length": int(match[1]),
                        "type": match[2] or None,
                        "comment": match[4] or None,
                    }
                }
            )

        qso_reports.append(qso_report)

    return {
        "header": header,
        "qso_reports": qso_reports,
    }


def main_loop_tuple(adif_file: TextIOWrapper) -> tuple[Header, list[QSOReport]]:
    header = Header()
    qso_reports: list[QSOReport] = []

    text = adif_file.read()

    header_match = re.match(HEADER_MATCH, text)
    header.full_header = header_match.group(1)

    header_matches = re.findall(pattern=TAG_MATCH, string=header.full_header)

    for match in header_matches:
        tag, _, _, value_opt_1, _, value_opt_2 = match

        header.assign_tag(
            tag=tag,
            value=value_opt_1 or value_opt_2,
        )

    records = re.findall(RECORD_MATCH, text[header_match.end(0) :])
    for record in records:
        qso_report = QSOReport()
        qso_report.full_report = record

        matches = re.findall(pattern=TAG_MATCH, string=record)

        for match in matches:
            qso_report.assign_tag(
                tag=match[0],
                value=match[3] or match[5],
                comment=match[4] or None,
            )

        qso_reports.append(qso_report)

    return header, qso_reports
