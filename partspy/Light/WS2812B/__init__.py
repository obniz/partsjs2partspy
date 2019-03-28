from attrdict import AttrDefault

class WS2812B:
    def __init__(self):
        self.keys = ['din', 'vcc', 'gnd']
        self.required_keys = ['din']

    @staticmethod
    def info():
        return AttrDefault(bool, {'name': 'WS2812B'})

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
        for i in range(0, 8, 2):
            byte = 0
            if val and 0x80 >> i:
                byte = one << 4
            else:
                byte = zero << 4
            if val and 0x80 >> (i + 1):
                byte |= one
            else:
                byte |= zero
            ret.push(*[byte])
        return ret

    @staticmethod
    def _generate_color(r, g, b):
        array = WS2812B._generate_from_byte(*[g])
        array = array.concat(*[WS2812B._generate_from_byte(*[r])])
        array = array.concat(*[WS2812B._generate_from_byte(*[b])])
        return array

    @staticmethod
    def _generate_hsv_color(h, s, v):
        C = v * s
        Hp = h / 60
        X = C * (1 - _math.abs(*[(_hp % 2 - 1)]))
        R = None
        G = None
        B = None
        if 0 <= _hp and _hp < 1:
            [R, G, B] = [C, X, 0]
        if 1 <= _hp and _hp < 2:
            [R, G, B] = [X, C, 0]
        if 2 <= _hp and _hp < 3:
            [R, G, B] = [0, C, X]
        if 3 <= _hp and _hp < 4:
            [R, G, B] = [0, X, C]
        if 4 <= _hp and _hp < 5:
            [R, G, B] = [X, 0, C]
        if 5 <= _hp and _hp < 6:
            [R, G, B] = [C, 0, X]
        m = (v - C)
        [R, G, B] = [(R + m), (G + m), (B + m)]
        R = _math.floor(*[R * 255])
        G = _math.floor(*[G * 255])
        B = _math.floor(*[B * 255])
        return WS2812B._generate_color(*[R, G, B])

    def rgb(self, r, g, b):
        self.spi.write(*[WS2812B._generate_color(*[r, g, b])])

    def hsv(self, h, s, v):
        self.spi.write(*[WS2812B._generate_hsv_color(*[h, s, v])])

    def rgbs(self, array):
        bytes = []
        for i in range(0, array.length, 1):
            oneArray = array[i]
            bytes = bytes.concat(*[WS2812B._generate_color(*[one_array[0], one_array[1], one_array[2]])])
        self.spi.write(*[bytes])

    def hsvs(self, array):
        bytes = []
        for i in range(0, array.length, 1):
            oneArray = array[i]
            bytes = bytes.concat(*[WS2812B._generate_hsv_color(*[one_array[0], one_array[1], one_array[2]])])
        self.spi.write(*[bytes])