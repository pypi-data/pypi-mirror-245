from dataclasses import dataclass
from datetime import date, datetime
from typing import get_args, get_type_hints

import maidenhead

from ..logger import logger


@dataclass
class QSOReport:
    full_report: str = ""

    # str attrs
    app_lotw_mode: str | None = None
    app_lotw_2xqsl: str | None = None
    app_lotw_npsunit: str | None = None
    app_lotw_owncall: str | None = None
    app_lotw_qslmode: str | None = None
    app_lotw_modegroup: str | None = None
    app_lotw_cqz_invalid: str | None = None
    app_lotw_cqz_inferred: str | None = None
    app_lotw_ituz_invalid: str | None = None
    app_lotw_ituz_inferred: str | None = None
    app_lotw_credit_granted: str | None = None
    app_lotw_dxcc_entity_status: str | None = None
    app_lotw_gridsquare_invalid: str | None = None
    app_lotw_my_cq_zone_inferre: str | None = None
    app_lotw_my_itu_zone_inferred: str | None = None
    app_lotw_my_dxcc_entity_status: str | None = None

    my_cnty: str | None = None
    my_state: str | None = None
    my_country: str | None = None
    my_latitude: float | None = None
    my_longitude: float | None = None
    my_cnty_human: str | None = None
    my_state_human: str | None = None

    pfx: str | None = None
    band: str | None = None
    call: str | None = None
    cnty: str | None = None
    iota: str | None = None
    mode: str | None = None
    state: str | None = None
    country: str | None = None
    submode: str | None = None
    latitude: float | None = None
    qsl_rcvd: str | None = None
    sat_name: str | None = None
    longitude: float | None = None
    prop_mode: str | None = None
    cnty_human: str | None = None
    state_human: str | None = None
    credit_granted: str | None = None
    station_callsign: str | None = None

    # other attrs
    _cqz = int | None

    @property
    def cqz(self) -> int | None:
        return self._cqz

    @cqz.setter
    def cqz(self, value: str) -> None:
        self._cqz = int(value)

    _dxcc: int | None = None

    @property
    def dxcc(self) -> int | None:
        return self._dxcc

    @dxcc.setter
    def dxcc(self, value: str) -> None:
        self._dxcc = int(value)

    _freq: float | None = None

    @property
    def freq(self) -> float | None:
        return self._freq

    @freq.setter
    def freq(self, value: str) -> None:
        self._freq = float(value)

    _ituz: int | None = None

    @property
    def ituz(self) -> int | None:
        return self._ituz

    @ituz.setter
    def ituz(self, value: str) -> None:
        self._ituz = int(value)

    _freq_rx: float | None = None

    @property
    def freq_rx(self) -> float | None:
        return self._freq_rx

    @freq_rx.setter
    def freq_rx(self, value: str) -> None:
        self._freq_rx = float(value)

    _time_on: int | None = None

    @property
    def time_on(self) -> int | None:
        return self._time_on

    @time_on.setter
    def time_on(self, value: str) -> None:
        self._time_on = int(value)

    _qslrdate: date | None = None

    @property
    def qslrdate(self) -> date | None:
        return self._qslrdate

    @qslrdate.setter
    def qslrdate(self, value: str) -> None:
        self._qslrdate = datetime.strptime(value, "%Y%m%d").date()

    _qso_date: int | None = None

    @property
    def qso_date(self) -> int | None:
        return self._qso_date

    @qso_date.setter
    def qso_date(self, value: str) -> None:
        self._qso_date = int(value)

    _my_gridsquare: str | None = None

    @property
    def my_gridsquare(self):
        return self._my_gridsquare

    @my_gridsquare.setter
    def my_gridsquare(self, value: str) -> None:
        self._my_gridsquare = value
        (
            self.my_latitude,
            self.my_longitude,
        ) = maidenhead.to_location(maiden=value, center=True)

    _gridsquare: str | None = None

    @property
    def gridsquare(self):
        return self._gridsquare

    @gridsquare.setter
    def gridsquare(self, value: str) -> None:
        self._gridsquare = value
        (
            self.latitude,
            self.longitude,
        ) = maidenhead.to_location(maiden=value, center=True)

    _my_dxcc: int | None = None

    @property
    def my_dxcc(self) -> int | None:
        return self._my_dxcc

    @my_dxcc.setter
    def my_dxcc(self, value: str) -> None:
        self._my_dxcc = int(value)

    _my_cq_zone: int | None = None

    @property
    def my_cq_zone(self) -> int | None:
        return self._my_cq_zone

    @my_cq_zone.setter
    def my_cq_zone(self, value: str) -> None:
        self._my_cq_zone = int(value)

    _my_itu_zone: int | None = None

    @property
    def my_itu_zone(self) -> int | None:
        return self._my_itu_zone

    @my_itu_zone.setter
    def my_itu_zone(self, value: str) -> None:
        self._my_itu_zone = int(value)

    _app_lotw_rxqsl: datetime | None = None

    @property
    def app_lotw_rxqsl(self) -> datetime | None:
        return self._app_lotw_rxqsl

    @app_lotw_rxqsl.setter
    def app_lotw_rxqsl(self, value: str) -> None:
        self._app_lotw_rxqsl = datetime.strptime(
            value,
            "%Y-%m-%d %H:%M:%S",
        )

    _app_lotw_rxqso: datetime | None = None

    @property
    def app_lotw_rxqso(self) -> datetime | None:
        return self._app_lotw_rxqso

    @app_lotw_rxqso.setter
    def app_lotw_rxqso(self, value: str) -> None:
        self._app_lotw_rxqso = datetime.strptime(
            value,
            "%Y-%m-%d %H:%M:%S",
        )

    _app_lotw_qso_timestamp: datetime | None = None

    @property
    def app_lotw_qso_timestamp(self) -> datetime | None:
        return self._app_lotw_qso_timestamp

    @app_lotw_qso_timestamp.setter
    def app_lotw_qso_timestamp(self, value: str) -> None:
        self._app_lotw_qso_timestamp = datetime.fromisoformat(value)

    def assign_tag(
        self,
        tag: str,
        value: str,
        comment: str | None = None,
    ) -> bool:
        # Special case tags that use comments in LoTW
        if tag == "MY_STATE":
            self.my_state = value
            self.my_state_human = comment or None
            return True
        elif tag == "MY_CNTY":
            self.my_cnty = value
            self.my_cnty_human = comment or None
            return True
        elif tag == "STATE":
            self.state = value
            self.state_human = comment or None
            return True
        elif tag == "CNTY":
            self.cnty = value
            self.cnty_human = comment or None
            return True

        # All other LoTW tags
        lowered_tag = tag.lower()
        if hasattr(self, lowered_tag):
            setattr(self, lowered_tag, value)
            return True

        logger.warn(f"Unknown tag: {tag}, {value}")
        return False
