# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if parse_version(kaitaistruct.__version__) < parse_version('0.9'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class Sanosat1(KaitaiStruct):
    """:field callsign: sanosat1_telemetry.body.callsign
    :field packet_type: sanosat1_telemetry.body.packet_type
    :field com_temperature: sanosat1_telemetry.body.com_temperature
    :field battery_voltage: sanosat1_telemetry.body.battery_voltage
    :field charging_current: sanosat1_telemetry.body.charging_current
    :field battery_temperature: sanosat1_telemetry.body.battery_temperature
    :field radiation_level: sanosat1_telemetry.body.radiation_level
    :field no_of_resets: sanosat1_telemetry.body.no_of_resets
    :field antenna_deployment_status: sanosat1_telemetry.body.antenna_deployment_status
    :field checksum_rtty_hex: sanosat1_telemetry.body.checksum_rtty_hex
    :field digimessage: sanosat1_telemetry.body.decision.digimessage
    :field digimessage: sanosat1_telemetry.body.decision.digimessage
    :field cwmessage: sanosat1_telemetry.body.decision.cwmessage
    :field com_temperature: sanosat1_telemetry.body.decision.com_temperature
    :field battery_temperature: sanosat1_telemetry.body.decision.battery_temperature
    :field charging_current: sanosat1_telemetry.body.decision.charging_current
    :field battery_voltage: sanosat1_telemetry.body.decision.battery_voltage
    :field antenna_deployed: sanosat1_telemetry.body.decision.antenna_deployed
    :field checksum_cw_hex: sanosat1_telemetry.body.decision.checksum_cw_hex
    """
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.sanosat1_telemetry = Sanosat1.Sanosat1TelemetryT(self._io, self, self._root)

    class WithDelimiter(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.delimiter = self._io.read_s4le()
            if not  ((self.delimiter == 65535)) :
                raise kaitaistruct.ValidationNotAnyOfError(self.delimiter, self._io, u"/types/with_delimiter/seq/0")
            self.callsign = (KaitaiStream.bytes_terminate(self._io.read_bytes(7), 0, False)).decode(u"ASCII")
            if not  ((self.callsign == u"AM9NPQ")) :
                raise kaitaistruct.ValidationNotAnyOfError(self.callsign, self._io, u"/types/with_delimiter/seq/1")
            self.packet_type = self._io.read_s2le()
            self.com_temperature = self._io.read_s2le()
            self.battery_voltage_hex_raw = self._io.read_s2le()
            self.charging_current = self._io.read_s2le()
            self.battery_temperature = self._io.read_s2le()
            self.radiation_level = self._io.read_s2le()
            self.no_of_resets = self._io.read_s2le()
            self.antenna_deployment_status = self._io.read_u1()

        @property
        def battery_voltage(self):
            if hasattr(self, '_m_battery_voltage'):
                return self._m_battery_voltage if hasattr(self, '_m_battery_voltage') else None

            self._m_battery_voltage = (self.battery_voltage_hex_raw / 100.00)
            return self._m_battery_voltage if hasattr(self, '_m_battery_voltage') else None


    class Rtty(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.callsign = (self._io.read_bytes_term(44, False, True, True)).decode(u"ASCII")
            if not  ((self.callsign == u"AM9NPQ") or (self.callsign == u"am9npq")) :
                raise kaitaistruct.ValidationNotAnyOfError(self.callsign, self._io, u"/types/rtty/seq/0")
            self.skip_dollar = self._io.read_s1()
            self.battery_temperature_raw = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.charging_current_raw = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.battery_voltage_before_dot_raw = (self._io.read_bytes_term(46, False, True, True)).decode(u"UTF-8")
            self.battery_voltage_after_dot_raw = (self._io.read_bytes_term(44, False, True, True)).decode(u"UTF-8")
            self.no_of_resets_raw = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.antenna_deployment_status_raw = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.radiation_level_raw = (self._io.read_bytes_term(63, False, True, True)).decode(u"utf8")
            self.checksum_rtty_raw = (self._io.read_bytes(2)).decode(u"UTF-8")

        @property
        def battery_temperature(self):
            if hasattr(self, '_m_battery_temperature'):
                return self._m_battery_temperature if hasattr(self, '_m_battery_temperature') else None

            self._m_battery_temperature = int(self.battery_temperature_raw)
            return self._m_battery_temperature if hasattr(self, '_m_battery_temperature') else None

        @property
        def battery_voltage_before_dot(self):
            if hasattr(self, '_m_battery_voltage_before_dot'):
                return self._m_battery_voltage_before_dot if hasattr(self, '_m_battery_voltage_before_dot') else None

            self._m_battery_voltage_before_dot = int(self.battery_voltage_before_dot_raw)
            return self._m_battery_voltage_before_dot if hasattr(self, '_m_battery_voltage_before_dot') else None

        @property
        def battery_voltage_after_dot(self):
            if hasattr(self, '_m_battery_voltage_after_dot'):
                return self._m_battery_voltage_after_dot if hasattr(self, '_m_battery_voltage_after_dot') else None

            self._m_battery_voltage_after_dot = int(self.battery_voltage_after_dot_raw)
            return self._m_battery_voltage_after_dot if hasattr(self, '_m_battery_voltage_after_dot') else None

        @property
        def battery_voltage(self):
            if hasattr(self, '_m_battery_voltage'):
                return self._m_battery_voltage if hasattr(self, '_m_battery_voltage') else None

            self._m_battery_voltage = ((self.battery_voltage_after_dot * 0.01) + self.battery_voltage_before_dot)
            return self._m_battery_voltage if hasattr(self, '_m_battery_voltage') else None

        @property
        def checksum_rtty_hex(self):
            if hasattr(self, '_m_checksum_rtty_hex'):
                return self._m_checksum_rtty_hex if hasattr(self, '_m_checksum_rtty_hex') else None

            self._m_checksum_rtty_hex = int(self.checksum_rtty_raw, 16)
            return self._m_checksum_rtty_hex if hasattr(self, '_m_checksum_rtty_hex') else None

        @property
        def radiation_level(self):
            if hasattr(self, '_m_radiation_level'):
                return self._m_radiation_level if hasattr(self, '_m_radiation_level') else None

            self._m_radiation_level = int(self.radiation_level_raw)
            return self._m_radiation_level if hasattr(self, '_m_radiation_level') else None

        @property
        def charging_current(self):
            if hasattr(self, '_m_charging_current'):
                return self._m_charging_current if hasattr(self, '_m_charging_current') else None

            self._m_charging_current = int(self.charging_current_raw)
            return self._m_charging_current if hasattr(self, '_m_charging_current') else None

        @property
        def antenna_deployment_status(self):
            if hasattr(self, '_m_antenna_deployment_status'):
                return self._m_antenna_deployment_status if hasattr(self, '_m_antenna_deployment_status') else None

            self._m_antenna_deployment_status = int(self.antenna_deployment_status_raw)
            return self._m_antenna_deployment_status if hasattr(self, '_m_antenna_deployment_status') else None

        @property
        def no_of_resets(self):
            if hasattr(self, '_m_no_of_resets'):
                return self._m_no_of_resets if hasattr(self, '_m_no_of_resets') else None

            self._m_no_of_resets = int(self.no_of_resets_raw)
            return self._m_no_of_resets if hasattr(self, '_m_no_of_resets') else None


    class DecisionDigiOrCw(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            _on = self.check
            if _on == 65535:
                self.decision = Sanosat1.DigiWithDelimiter(self._io, self, self._root)
            elif _on == 19777:
                self.decision = Sanosat1.Cw(self._io, self, self._root)
            elif _on == 28001:
                self.decision = Sanosat1.Cw(self._io, self, self._root)
            else:
                self.decision = Sanosat1.DigiWithoutDelimiter(self._io, self, self._root)

        @property
        def check(self):
            if hasattr(self, '_m_check'):
                return self._m_check if hasattr(self, '_m_check') else None

            _pos = self._io.pos()
            self._io.seek(0)
            self._m_check = self._io.read_u2le()
            self._io.seek(_pos)
            return self._m_check if hasattr(self, '_m_check') else None


    class WithoutDelimiter(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.callsign = (KaitaiStream.bytes_terminate(self._io.read_bytes(7), 0, False)).decode(u"ASCII")
            if not  ((self.callsign == u"AM9NPQ")) :
                raise kaitaistruct.ValidationNotAnyOfError(self.callsign, self._io, u"/types/without_delimiter/seq/0")
            self.packet_type = self._io.read_s2le()
            self.com_temperature = self._io.read_s2le()
            self.battery_voltage_hex_raw = self._io.read_s2le()
            self.charging_current = self._io.read_s2le()
            self.battery_temperature = self._io.read_s2le()
            self.radiation_level = self._io.read_s2le()
            self.no_of_resets = self._io.read_s2le()
            self.antenna_deployment_status = self._io.read_u1()

        @property
        def battery_voltage(self):
            if hasattr(self, '_m_battery_voltage'):
                return self._m_battery_voltage if hasattr(self, '_m_battery_voltage') else None

            self._m_battery_voltage = (self.battery_voltage_hex_raw / 100.00)
            return self._m_battery_voltage if hasattr(self, '_m_battery_voltage') else None


    class DigiWithoutDelimiter(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.header = (self._io.read_bytes(3)).decode(u"ASCII")
            if not  ((self.header == u"NPQ")) :
                raise kaitaistruct.ValidationNotAnyOfError(self.header, self._io, u"/types/digi_without_delimiter/seq/0")
            self.digimessage = (self._io.read_bytes_full()).decode(u"UTF-8")


    class Cw(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.callsign = (self._io.read_bytes(6)).decode(u"ASCII")
            if not  ((self.callsign == u"AM9NPQ") or (self.callsign == u"am9npq")) :
                raise kaitaistruct.ValidationNotAnyOfError(self.callsign, self._io, u"/types/cw/seq/0")
            self.cwmessage = (self._io.read_bytes_full()).decode(u"UTF-8")

        @property
        def battery_temperature(self):
            if hasattr(self, '_m_battery_temperature'):
                return self._m_battery_temperature if hasattr(self, '_m_battery_temperature') else None

            self._m_battery_temperature = ((int((self.cwmessage)[self.length_of_obc_temp:(self.length_of_obc_temp + self.length_of_bat_temp)]) * -1) if self.sign_of_bat_temp == u"-" else int((self.cwmessage)[self.length_of_obc_temp:(self.length_of_obc_temp + self.length_of_bat_temp)]))
            return self._m_battery_temperature if hasattr(self, '_m_battery_temperature') else None

        @property
        def residuals(self):
            if hasattr(self, '_m_residuals'):
                return self._m_residuals if hasattr(self, '_m_residuals') else None

            self._m_residuals = int((self.cwmessage)[(self.length_of_cwmessage - 5):(self.length_of_cwmessage - 3)], 16)
            return self._m_residuals if hasattr(self, '_m_residuals') else None

        @property
        def battery_voltage(self):
            if hasattr(self, '_m_battery_voltage'):
                return self._m_battery_voltage if hasattr(self, '_m_battery_voltage') else None

            self._m_battery_voltage = (int((self.cwmessage)[((self.length_of_obc_temp + self.length_of_bat_temp) + self.length_of_current):(((self.length_of_obc_temp + self.length_of_bat_temp) + self.length_of_current) + 2)]) * 0.1)
            return self._m_battery_voltage if hasattr(self, '_m_battery_voltage') else None

        @property
        def sign_of_obc_temp(self):
            if hasattr(self, '_m_sign_of_obc_temp'):
                return self._m_sign_of_obc_temp if hasattr(self, '_m_sign_of_obc_temp') else None

            self._m_sign_of_obc_temp = (u"+" if ((self.residuals & 64) >> 6) == 0 else u"-")
            return self._m_sign_of_obc_temp if hasattr(self, '_m_sign_of_obc_temp') else None

        @property
        def antenna_deployed(self):
            if hasattr(self, '_m_antenna_deployed'):
                return self._m_antenna_deployed if hasattr(self, '_m_antenna_deployed') else None

            self._m_antenna_deployed = (True if ((self.residuals & 128) >> 7) == 1 else False)
            return self._m_antenna_deployed if hasattr(self, '_m_antenna_deployed') else None

        @property
        def length_of_obc_temp(self):
            if hasattr(self, '_m_length_of_obc_temp'):
                return self._m_length_of_obc_temp if hasattr(self, '_m_length_of_obc_temp') else None

            self._m_length_of_obc_temp = (((self.length_of_cwmessage - 7) - self.length_of_current) - self.length_of_bat_temp)
            return self._m_length_of_obc_temp if hasattr(self, '_m_length_of_obc_temp') else None

        @property
        def charging_current(self):
            if hasattr(self, '_m_charging_current'):
                return self._m_charging_current if hasattr(self, '_m_charging_current') else None

            self._m_charging_current = int((self.cwmessage)[(self.length_of_obc_temp + self.length_of_bat_temp):((self.length_of_obc_temp + self.length_of_bat_temp) + self.length_of_current)])
            return self._m_charging_current if hasattr(self, '_m_charging_current') else None

        @property
        def length_of_bat_temp(self):
            if hasattr(self, '_m_length_of_bat_temp'):
                return self._m_length_of_bat_temp if hasattr(self, '_m_length_of_bat_temp') else None

            self._m_length_of_bat_temp = ((self.residuals & 3) >> 0)
            return self._m_length_of_bat_temp if hasattr(self, '_m_length_of_bat_temp') else None

        @property
        def length_of_cwmessage(self):
            if hasattr(self, '_m_length_of_cwmessage'):
                return self._m_length_of_cwmessage if hasattr(self, '_m_length_of_cwmessage') else None

            self._m_length_of_cwmessage = len(self.cwmessage)
            return self._m_length_of_cwmessage if hasattr(self, '_m_length_of_cwmessage') else None

        @property
        def checksum_cw_hex(self):
            if hasattr(self, '_m_checksum_cw_hex'):
                return self._m_checksum_cw_hex if hasattr(self, '_m_checksum_cw_hex') else None

            self._m_checksum_cw_hex = int((self.cwmessage)[(self.length_of_cwmessage - 2):self.length_of_cwmessage], 16)
            return self._m_checksum_cw_hex if hasattr(self, '_m_checksum_cw_hex') else None

        @property
        def length_of_current(self):
            if hasattr(self, '_m_length_of_current'):
                return self._m_length_of_current if hasattr(self, '_m_length_of_current') else None

            self._m_length_of_current = ((self.residuals & 28) >> 2)
            return self._m_length_of_current if hasattr(self, '_m_length_of_current') else None

        @property
        def sign_of_bat_temp(self):
            if hasattr(self, '_m_sign_of_bat_temp'):
                return self._m_sign_of_bat_temp if hasattr(self, '_m_sign_of_bat_temp') else None

            self._m_sign_of_bat_temp = (u"+" if ((self.residuals & 32) >> 5) == 0 else u"-")
            return self._m_sign_of_bat_temp if hasattr(self, '_m_sign_of_bat_temp') else None

        @property
        def com_temperature(self):
            if hasattr(self, '_m_com_temperature'):
                return self._m_com_temperature if hasattr(self, '_m_com_temperature') else None

            self._m_com_temperature = ((int((self.cwmessage)[0:self.length_of_obc_temp]) * -1) if self.sign_of_obc_temp == u"-" else int((self.cwmessage)[0:self.length_of_obc_temp]))
            return self._m_com_temperature if hasattr(self, '_m_com_temperature') else None


    class Sanosat1TelemetryT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            _on = self.check
            if _on == 2606547689692286273:
                self.body = Sanosat1.Rtty(self._io, self, self._root)
            elif _on == 2606583012040207713:
                self.body = Sanosat1.Rtty(self._io, self, self._root)
            elif _on == 5636621350199164927:
                self.body = Sanosat1.WithDelimiter(self._io, self, self._root)
            elif _on == 72146999389539649:
                self.body = Sanosat1.WithoutDelimiter(self._io, self, self._root)
            else:
                self.body = Sanosat1.DecisionDigiOrCw(self._io, self, self._root)

        @property
        def check(self):
            if hasattr(self, '_m_check'):
                return self._m_check if hasattr(self, '_m_check') else None

            _pos = self._io.pos()
            self._io.seek(0)
            self._m_check = self._io.read_u8le()
            self._io.seek(_pos)
            return self._m_check if hasattr(self, '_m_check') else None


    class DigiWithDelimiter(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.delimiter = self._io.read_s4le()
            if not  ((self.delimiter == 65535)) :
                raise kaitaistruct.ValidationNotAnyOfError(self.delimiter, self._io, u"/types/digi_with_delimiter/seq/0")
            self.header = (self._io.read_bytes(3)).decode(u"ASCII")
            if not  ((self.header == u"NPQ")) :
                raise kaitaistruct.ValidationNotAnyOfError(self.header, self._io, u"/types/digi_with_delimiter/seq/1")
            self.digimessage = (self._io.read_bytes_full()).decode(u"UTF-8")



