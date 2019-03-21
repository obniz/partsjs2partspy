import datetime

class GYSFDMAXB:
    def __init__(self):
        self.keys = ['vcc', 'txd', 'rxd', 'gnd', 'Opps']
        self.required_keys = ['txd', 'rxd']
        self.io_keys = self.keys
        self.display_name = 'gps'
        self.display_io_names = {'txd': 'txd', 'rxd': 'rxd', '_opps': '1pps'}

    @staticmethod
    def info():
        return {'name': 'GYSFDMAXB'}

    def wired(self, obniz):
        self.obniz = obniz
        self.tx = self.params.txd
        self.rx = self.params.rxd
        self.vcc = self.params.vcc
        self.gnd = self.params.gnd
        self._opps = self.params._opps
        self.obniz.set_vcc_gnd(*[self.params.vcc, self.params.gnd, '5v'])
        self.uart = obniz.get_free_uart()
        self.uart.start(*[{'tx': self.params.txd, 'rx': self.params.rxd, 'baud': 9600, 'drive': '3v'}])
        self.edited_data = }
        self.edited_data.enable = False
        self.edited_data.GPGSV = [0] * 4
        self.on1pps = null
        self.last1pps = 0
        self.gps_info = }
        self.gps_info._sentence_type = {'GPGGA': 0x0001, 'GPGSA': 0x0002, 'GPGSV': 0x0004, 'GPRMC': 0x0008, 'GPVTG': 0x0010, 'GPZDA': 0x0020}
        self.gps_info.status = 'V'
        self.gps_info.sentences = []
        self.gps_info.satellite_info = {'satellites': [], 'in_view': 0}

    def start1pps(self, callback):
        self.on1pps = callback
        if callback:
            self.last1pps = 2
            self.obniz.get_ad(*[self._opps]).self = self
            self.obniz.get_ad(*[self._opps]).start(*[# TODO: failed to generate Function Expression])
        else:
            self.obniz.get_ad(*[self._opps]).end()

    def read_sentence(self):
        results = []
        if self.uart.is_data_exists():
            pos = self.uart.received.index_of(*[0x0a])
            if pos >= 0:
                results = self.uart.received.slice(*[0, pos - 1])
                self.uart.received.splice(*[0, pos + 1])
                return self.uart.try_convert_string(*[results])
        return ''

    def get_edited_data(self):
        n = None
        utc = None
        format = None
        sentence = self.read_sentence()
        self.edited_data.enable = False
        self.edited_data.GPGSV = [0] * 4
        while sentence.length > 0:
            part = sentence.split(*[','])
            if sentence.slice(*[-4, -3]) != ',':
                st = part[part.length - 1].slice(*[0, -3])
                part.push(*[part[part.length - 1].slice(*[-3])])
                part[part.length - 2] = st
            self.edited_data.sentence = part.join(*[','])
            if part[0]=='$GPGGA':
                self.edited_data.GPGGA = part
            elif part[0]=='$GPGLL':
                self.edited_data.GPGLL = part
            elif part[0]=='$GPGSA':
                self.edited_data.GPGSA = part
            elif part[0]=='$GPGSV':
                n = _number(*[part[2]])
                if n > self.edited_data.GPGSV.length:
                    while n > self.edited_data.GPGSV.length:
                        self.edited_data.GPGSV.push(*[[]])
                self.edited_data.GPGSV[n - 1] = part
            elif part[0]=='$GPRMC':
                self.edited_data.GPRMC = part
            elif part[0]=='$GPVTG':
                self.edited_data.GPVTG = part
            elif part[0]=='$GPZDA':
                self.edited_data.GPZDA = part
                utc = str(str(str(str(str(str(part[4]) + '/' + part[3]) + '/' + part[2]) + ' ' + part[1].substring(*[0, 2])) + ':' + part[1].substring(*[2, 4])) + ':' + part[1].substring(*[4, 6])) + ' +00:00'
                self.edited_data.timestamp = datetime.datetime.now()
            else:
                format = part[0].substr(*[1])
                self.edited_data[format] = part
            self.edited_data.enable = True
            sentence = self.read_sentence()
        return self.edited_data

    def get_gps_info(self, edited_data):
        NMEA_SATINSENTENCE = 4
        NMEA_MAXSAT = 12
        edited_data = edited_data or self.get_edited_data()
        self.gps_info.status = 'V'
        if edited_data.enable:
            if edited_data.GPGGA:
                gga = edited_data.GPGGA
                self.gps_info.gps_quality = parse_float(*[gga[6]])
                self.gps_info.hdop = parse_float(*[gga[8]])
                self.gps_info.altitude = parse_float(*[gga[9]])
                latitude = self.nmea2dd(*[parse_float(*[gga[2]])])
                self.gps_info.latitude = latitude if gga[3] == 'N' else -latitude
                longitude = self.nmea2dd(*[parse_float(*[gga[4]])])
                self.gps_info.longitude = longitude if gga[5] == 'E' else -longitude
                self.gps_info.sentences.add(*[self.gps_info._sentence_type.GPGGA])
            if edited_data.GPGSV:
                for n in range(0, edited_data.GPGSV.length, 1):

                # TODO: failed to generate FOR statement
            if edited_data.GPGSA:
                gsa = edited_data.GPGSA
                nuse = 0
                self.gps_info.fix_mode = parse_float(*[gsa[2]])
                self.gps_info.pdop = parse_float(*[gsa[15]])
                self.gps_info.hdop = parse_float(*[gsa[16]])
                self.gps_info.vdop = parse_float(*[gsa[17]])
                for i in range(0, NMEA_MAXSAT, 1):
                    for j in range(0, self.gps_info.satellite_info.in_view, 1):
                        if self.gps_info.satellite_info.satellites[j] and gsa[i + 3] == self.gps_info.satellite_info.satellites[j].id:
                            self.gps_info.satellite_info.satellites[j].in_use = True

                self.gps_info.satellite_info.in_use = nuse
                self.gps_info.sentences.add(*[self.gps_info._sentence_type.GPGSA])
            if edited_data.GPRMC:
                rmc = edited_data.GPRMC
                self.gps_info.status = rmc[2]
                latitude = self.nmea2dd(*[parse_float(*[rmc[3]])])
                self.gps_info.latitude = latitude if rmc[4] == 'N' else -latitude
                longitude = self.nmea2dd(*[parse_float(*[rmc[5]])])
                self.gps_info.longitude = longitude if rmc[6] == 'E' else -longitude
                NMEA_TUD_KNOTS = 1.852
                self.gps_info.speed = parse_float(*[rmc[7]]) * NMEA_TUD_KNOTS
                self.gps_info.direction = rmc[8]
                self.gps_info.sentences.add(*[self.gps_info._sentence_type.GPRMC])
            if edited_data.GPVTG:
                vtg = edited_data.GPVTG
                self.gps_info.direction = parse_float(*[vtg[1]])
                self.gps_info.declination = parse_float(*[vtg[3]])
                self.gps_info.speed = parse_float(*[vtg[7]])
                self.gps_info.sentences.add(*[self.gps_info._sentence_type.GPVTG])
            if edited_data.GPZDA:
                self.gps_info.utc = edited_data.timestamp
                self.gps_info.sentences.add(*[self.gps_info._sentence_type.GPZDA])
        return self.gps_info

    def latitude(self):
        return self.nmea2dd(*[self._latitude])

    def longitude(self):
        return self.nmea2dd(*[self._longitude])

    def _mnea_to(self, format, value):
        result = self.nmea2dd(*[value])
        if type(format) == 'string':
            if format.to_upper_case()=='DMS':
                result = self.nmea2dms(*[value])
            elif format.to_upper_case()=='DM':
                result = self.nmea2dm(*[value])
            elif format.to_upper_case()=='S':
                result = self.nmea2s(*[value])
            else:

        return result

    def latitude_to(self, format):
        return self._mnea_to(*[format, self._latitude])

    def longitude_to(self, format):
        return self._mnea_to(*[format, self._longitude])

    def status2string(self, status):
        status = status or self.status
        if status == 'A':
            return 'Active'
        if status == 'V':
            return 'Void'
        return status

    def fix_mode2string(self, fix_mode):
        fix_mode = fix_mode or self.fix_mode
        if fix_mode == 1:
            return 'Fix not available'
        if fix_mode == 2:
            return '2D'
        if fix_mode == 3:
            return '3D'
        return fix_mode

    def gps_quality2string(self, gps_quality):
        gps_quality = gps_quality or self.gps_quality
        if gps_quality == 0:
            return 'Invalid'
        if gps_quality == 1:
            return 'GPS fix'
        if gps_quality == 2:
            return 'DGPS fix'
        return gps_quality

    def nmea2dms(self, val):
        val = parse_float(*[val])
        d = _math.floor(*[val / 100])
        m = _math.floor(*[val / 100.0 - d * 100.0])
        s = val / 100.0 - d * 100.0 - m * 60
        return str(str(str(d) + '°' + m) + "'" + s.to_fixed(*[1])) + '"'

    def nmea2dm(self, val):
        val = parse_float(*[val])
        d = _math.floor(*[val / 100.0])
        m = val / 100.0 - d * 100.0
        return str(str(d) + '°' + m.to_fixed(*[4])) + "'"

    def nmea2dd(self, val):
        val = parse_float(*[val])
        d = _math.floor(*[val / 100.0])
        m = _math.floor(*[val / 100.0 - d * 100.0 / 60])
        s = val / 100.0 - d * 100.0 - m * 60 / 60 * 60
        return parse_float(*[d + m + s.to_fixed(*[6])])

    def nmea2s(self, val):
        val = parse_float(*[val])
        d = _math.floor(*[val / 100.0])
        m = _math.floor(*[val / 100.0 - d * 100.0 / 60])
        s = val / 100.0 - d * 100.0 - m * 60 / 60 * 60
        return d + m + s / 1.0 / 60.0 / 60.0