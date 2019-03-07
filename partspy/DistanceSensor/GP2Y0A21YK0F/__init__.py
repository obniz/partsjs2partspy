import asyncio

class _gp2_y0_a21_yk0_f:
    def __init__(self):
        self.keys = ['vcc', 'gnd', 'signal']
        self.required_keys = ['signal']
        self.display_io_names = {'vcc': 'vcc', 'gnd': 'gnd', 'signal': 'signal'}
        self._unit = 'mm'

    @staticmethod
    def info():
        return {'name': 'GP2Y0A21YK0F'}

    def wired(self, obniz):
        self.obniz = obniz
        obniz.set_vcc_gnd(*[self.params.vcc, self.params.gnd, '5v'])
        self.io_signal = obniz.get_io(*[self.params.signal])
        self.io_signal.end()
        self.ad_signal = obniz.get_ad(*[self.params.signal])

    def start(self, callback):
        self.ad_signal.start(*[# TODO: ArrowFunctionExpression was here])

    def _volt2distance(self, val):
        if val <= 0:
            val = 0.001
        distance = 19988.34 * _math.pow(*[val / 5.0 * 1024, -1.25214]) * 10
        if self._unit == 'mm':
            distance = parse_int(*[distance * 10]) / 10
        else:
            distance = parse_int(*[distance * 10]) / 10
        return distance

    def get_wait(self):
        return await# TODO: ArrowFunctionExpression was here

    def unit(self, unit):
        if unit == 'mm':
            self._unit = 'mm'
        elif unit == 'inch':
            self._unit = 'inch'
        else:
            self._unit = 'inch'