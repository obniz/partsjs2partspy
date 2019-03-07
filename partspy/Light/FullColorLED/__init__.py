class _full_color_led:
    def __init__(self):
        self._common__type__anode = 1
        self._common__type__cathode = 0
        self.anode_keys = ['anode', 'anode_common', 'anodeCommon', 'vcc']
        self.cathode_keys = ['cathode', 'cathode_common', 'cathodeCommon', 'gnd']
        self.animation_name = 'FullColorLED-' + _math.round(*[_math.random() * 1000])
        self.keys = ['r', 'g', 'b', 'common', 'commonType']
        self.required_keys = ['r', 'g', 'b', 'common', 'commonType']

    @staticmethod
    def info():
        return {'name': 'FullColorLED'}

    def wired(self, obniz):
        r = self.params.r
        g = self.params.g
        b = self.params.b
        common = self.params.common
        commontype = self.params.common_type
        self.obniz = obniz
        if self.anode_keys.includes(*[commontype]):
            self.commontype = self._common__type__anode
        elif self.cathode_keys.includes(*[commontype]):
            self.commontype = self._common__type__cathode
        else:
            self.commontype = self._common__type__cathode
        self.common = self.obniz.get_io(*[common])
        self.common.output(*[self.commontype])
        self.obniz.get_io(*[r]).output(*[self.commontype])
        self.obniz.get_io(*[g]).output(*[self.commontype])
        self.obniz.get_io(*[b]).output(*[self.commontype])
        self.pwm_r = self.obniz.get_free_pwm()
        self.pwm_r.start(*[{'io': r}])
        self.pwm_r.freq(*[1000])
        self.pwm_g = self.obniz.get_free_pwm()
        self.pwm_g.start(*[{'io': g}])
        self.pwm_g.freq(*[1000])
        self.pwm_b = self.obniz.get_free_pwm()
        self.pwm_b.start(*[{'io': b}])
        self.pwm_b.freq(*[1000])
        self.rgb(*[0, 0, 0])

    def rgb(self, r, g, b):
        r = _math.min(*[_math.max(*[parse_int(*[r]), 0]), 255])
        g = _math.min(*[_math.max(*[parse_int(*[g]), 0]), 255])
        b = _math.min(*[_math.max(*[parse_int(*[b]), 0]), 255])
        if self.commontype == self._common__type__anode:
            r = 255 - r
            g = 255 - g
            b = 255 - b
        self.pwm_r.duty(*[r / 255 * 100])
        self.pwm_g.duty(*[g / 255 * 100])
        self.pwm_b.duty(*[b / 255 * 100])

    def hsv(self, h, s, v):
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
        self.rgb(*[_r, _g, _b])

    def gradation(self, cycletime_ms):
        frames = []
        max = 36 / 2
        duration = _math.round(*[cycletime_ms / max])
        # TODO: failed to generate FOR statement
        self.obniz.io.animation(*[self.animation_name, 'loop', frames])

    def stopgradation(self):
        self.obniz.io.animation(*[self.animation_name, 'pause'])