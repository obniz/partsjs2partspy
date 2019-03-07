class _ws2812_b:
    def __init__(self):
        self.keys = ['din', 'vcc', 'gnd']
        self.required_keys = ['din']

    @staticmethod
    def info():
        return {'name': 'WS2812B'}

    def wired(self, obniz):
        self.obniz = obniz
        obniz.set_vcc_gnd(*[self.params.vcc, self.params.gnd, '5v'])
        self.params.mode = 'master'
        self.params.frequency = parse_int(*[3.33 * 1000 * 1000])
        self.params.mosi = self.params.din
        self.params.drive = '5v'
        self.spi = self.obniz.get_spi_with_config(*[self.params])

    @staticmethod
    def _generate_from_byte(val):
        val = parse_int(*[val])
        zero = 0x8
        one = 0xe
        ret = []
        # TODO: failed to generate FOR statement
        return ret

    @staticmethod
    def _generate_color(r, g, b):
        array = _ws2812_b._generate_from_byte(*[g])
        array = array.concat(*[_ws2812_b._generate_from_byte(*[r])])
        array = array.concat(*[_ws2812_b._generate_from_byte(*[b])])
        return array

    @staticmethod
    def _generate_hsv_color(h, s, v):
        C = v * s
        Hp = h / 60
        X = _c * 1 - _math.abs(*[_hp % 2 - 1])
        R = None
        G = None
        B = None
        if 0 <= _hp and _hp < 1:
            [_r, _g, _b] = [_c, _x, 0]
        if 1 <= _hp and _hp < 2:
            [_r, _g, _b] = [_x, _c, 0]
        if 2 <= _hp and _hp < 3:
            [_r, _g, _b] = [0, _c, _x]
        if 3 <= _hp and _hp < 4:
            [_r, _g, _b] = [0, _x, _c]
        if 4 <= _hp and _hp < 5:
            [_r, _g, _b] = [_x, 0, _c]
        if 5 <= _hp and _hp < 6:
            [_r, _g, _b] = [_c, 0, _x]
        m = v - _c
        [_r, _g, _b] = [_r + m, _g + m, _b + m]
        _r = _math.floor(*[_r * 255])
        _g = _math.floor(*[_g * 255])
        _b = _math.floor(*[_b * 255])
        return _ws2812_b._generate_color(*[_r, _g, _b])

    def rgb(self, r, g, b):
        self.spi.write(*[_ws2812_b._generate_color(*[r, g, b])])

    def hsv(self, h, s, v):
        self.spi.write(*[_ws2812_b._generate_hsv_color(*[h, s, v])])

    def rgbs(self, array):
        bytes = []
        # TODO: failed to generate FOR statement
        self.spi.write(*[bytes])

    def hsvs(self, array):
        bytes = []
        # TODO: failed to generate FOR statement
        self.spi.write(*[bytes])