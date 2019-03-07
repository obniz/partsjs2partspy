class _pa_pirs_vz:
    def __init__(self):
        self.keys = ['vcc', 'gnd', 'signal']
        self.required_keys = ['signal']

    @staticmethod
    def info():
        return {'name': 'PaPIRsVZ'}

    def wired(self, obniz):
        self.obniz = obniz
        self.io_signal = obniz.get_io(*[self.params.signal])
        self.io_signal.pull(*['0v'])
        obniz.set_vcc_gnd(*[self.params.vcc, self.params.gnd, '5v'])
        self.io_signal.input(*[# TODO: ArrowFunctionExpression was here])