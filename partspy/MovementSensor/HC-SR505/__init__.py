class _hcsr505:
    def __init__(self):
        self.keys = ['vcc', 'gnd', 'signal']
        self.required_keys = ['signal']

    @staticmethod
    def info():
        return {'name': 'HC-SR505'}

    def wired(self, obniz):
        self.obniz = obniz
        self.io_signal = obniz.get_io(*[self.params.signal])
        obniz.set_vcc_gnd(*[self.params.vcc, self.params.gnd, '5v'])
        self.io_signal.input(*[# TODO: ArrowFunctionExpression was here])

    def get_wait(self):
        return self.io_signal.input_wait()