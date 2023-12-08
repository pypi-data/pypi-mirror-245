import re
from datetime import datetime

import maidenhead

from ..dataclasses import QSOReport
from ..logger import setup_logger

COMMENT_MATCH = re.compile(r"^(.*?)\s*//\s*(.*)$")

logger = setup_logger()


def match_report_tag(qso_report: QSOReport, tag_str: str, value: str) -> None:
    comment: str | None = None
    comment_match = re.match(pattern=COMMENT_MATCH, string=value)
    if comment_match:
        value = comment_match.group(1)
        comment = comment_match.group(2)

    match tag_str:
        case "APP_LoTW_OWNCALL":
            qso_report.app_lotw_owncall = value
        case "STATION_CALLSIGN":
            qso_report.station_callsign = value
        case "MY_DXCC":
            qso_report.my_dxcc = int(value)
        case "MY_COUNTRY":
            qso_report.my_country = value
        case "APP_LoTW_MY_DXCC_ENTITY_STATUS":
            qso_report.app_lotw_dxcc_entity_status = value
        case "MY_GRIDSQUARE":
            qso_report.my_gridsquare = value
            (
                qso_report.my_latitude,
                qso_report.my_longitude,
            ) = maidenhead.to_location(maiden=value, center=True)
        case "MY_STATE":
            qso_report.my_state = value
            qso_report.my_state_human = comment or qso_report.my_state
        case "MY_CNTY":
            qso_report.my_cnty = value
            qso_report.my_cnty_human = comment or qso_report.my_cnty_human
        case "MY_CQ_ZONE":
            qso_report.my_cq_zone = int(value)
        case "MY_ITU_ZONE":
            qso_report.my_itu_zone = int(value)
        case "CALL":
            qso_report.call = value
        case "BAND":
            qso_report.band = value
        case "FREQ":
            qso_report.freq = float(value)
        case "MODE":
            qso_report.mode = value
        case "APP_LoTW_MODEGROUP":
            qso_report.app_lotw_modegroup = value
        case "QSO_DATE":
            qso_report.qso_date = int(value)
        case "APP_LoTW_RXQSO":
            qso_report.app_lotw_rxqso = datetime.strptime(
                value,
                "%Y-%m-%d %H:%M:%S",
            )
        case "TIME_ON":
            qso_report.time_on = int(value)
        case "APP_LoTW_QSO_TIMESTAMP":
            qso_report.app_lotw_qso_timestamp = datetime.fromisoformat(value)
        case "QSL_RCVD":
            qso_report.qsl_rcvd = value
        case "QSLRDATE":
            qso_report.qslrdate = datetime.strptime(value, "%Y%m%d").date()
        case "APP_LoTW_RXQSL":
            qso_report.app_lotw_rxqsl = datetime.strptime(
                value,
                "%Y-%m-%d %H:%M:%S",
            )
        case "DXCC":
            qso_report.dxcc = int(value)
        case "COUNTRY":
            qso_report.country = value
        case "APP_LoTW_DXCC_ENTITY_STATUS":
            qso_report.app_lotw_dxcc_entity_status = value
        case "PFX":
            qso_report.pfx = str(value)
        case "APP_LoTW_2xQSL":
            qso_report.app_lotw_2xqsl = value
        case "GRIDSQUARE":
            qso_report.gridsquare = value
            qso_report.latitude, qso_report.longitude = maidenhead.to_location(
                maiden=value,
                center=True,
            )
        case "CQZ":
            qso_report.cqz = int(value)
        case "ITUZ":
            qso_report.ituz = int(value)
        case "STATE":
            qso_report.state = value
            qso_report.state_human = comment or qso_report.state_human
        case "CNTY":
            qso_report.cnty = value
            qso_report.cnty_human = comment or qso_report.cnty_human
        case "APP_LoTW_CREDIT_GRANTED":
            qso_report.app_lotw_credit_granted = value
        case "CREDIT_GRANTED":
            qso_report.credit_granted = value
        case "APP_LoTW_ITUZ_Inferred":
            qso_report.app_lotw_ituz_inferred = value
        case "APP_LoTW_CQZ_Inferred":
            qso_report.app_lotw_cqz_inferred = value
        case "APP_LoTW_CQZ_Invalid":
            qso_report.app_lotw_cqz_invalid = value
        case "APP_LoTW_ITUZ_Invalid":
            qso_report.app_lotw_ituz_invalid = value
        case "APP_LoTW_MY_CQ_ZONE_Inferre":
            qso_report.app_lotw_cqz_invalid = value
        case "APP_LoTW_MY_ITU_ZONE_Inferred":
            qso_report.app_lotw_ituz_inferred = value
        case "FREQ_RX":
            qso_report.freq_rx = float(value)
        case "IOTA":
            qso_report.iota = value
        case "SUBMODE":
            qso_report.submode = value
        case "PROP_MODE":
            qso_report.prop_mode = value
        case "APP_LoTW_NPSUNIT":
            qso_report.app_lotw_npsunit = value
        case "APP_LoTW_QSLMODE":
            qso_report.app_lotw_qslmode = value
        case "APP_LoTW_MODE":
            qso_report.app_lotw_mode = value
        case "SAT_NAME":
            qso_report.sat_name = value
        case "APP_LoTW_GRIDSQUARE_Invalid":
            qso_report.app_lotw_gridsquare_invalid = value
        case _:
            logger.warn(f"Unknown tag: {tag_str}, {value}")
