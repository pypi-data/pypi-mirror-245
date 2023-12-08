from dataclasses import dataclass
from datetime import date, datetime


@dataclass
class QSOReport:
    full_report: str = ""

    app_lotw_owncall: str | None = None
    station_callsign: str | None = None
    my_dxcc: int | None = None
    my_country: str | None = None
    app_lotw_my_dxcc_entity_status: str | None = None
    my_gridsquare: str | None = None
    my_latitude: float | None = None
    my_longitude: float | None = None
    my_state: str | None = None
    my_state_human: str | None = None
    my_cnty: str | None = None
    my_cnty_human: str | None = None
    my_cq_zone: int | None = None
    my_itu_zone: int | None = None
    call: str | None = None
    band: str | None = None
    freq: float | None = None
    mode: str | None = None
    app_lotw_modegroup: str | None = None
    qso_date: int | None = None
    # QSO record inserted/modified at LoTW
    app_lotw_rxqso: datetime | None = None
    time_on: int | None = None
    # QSO Date & Time; ISO-8601
    app_lotw_qso_timestamp: datetime | None = None
    qsl_rcvd: str | None = None
    # 20231204
    qslrdate: date | None = None
    # QSL record matched/modified at LoTW
    app_lotw_rxqsl: datetime | None = None
    dxcc: int | None = None
    country: str | None = None
    app_lotw_dxcc_entity_status: str | None = None
    pfx: str | None = None
    app_lotw_2xqsl: str | None = None
    gridsquare: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    cqz: int | None = None
    ituz: int | None = None
    state: str | None = None
    state_human: str | None = None
    cnty: str | None = None
    cnty_human: str | None = None
    app_lotw_credit_granted: str | None = None
    credit_granted: str | None = None
    app_lotw_ituz_inferred: str | None = None
    app_lotw_cqz_inferred: str | None = None
    app_lotw_cqz_invalid: str | None = None
    app_lotw_ituz_invalid: str | None = None
    app_lotw_my_cq_zone_inferre: str | None = None
    app_lotw_my_itu_zone_inferred: str | None = None
    freq_rx: float | None = None
    iota: str | None = None
    submode: str | None = None
    sat_name: str | None = None
    prop_mode: str | None = None
    app_lotw_npsunit: str | None = None
    app_lotw_mode: str | None = None
    app_lotw_qslmode: str | None = None
    app_lotw_gridsquare_invalid: str | None = None
