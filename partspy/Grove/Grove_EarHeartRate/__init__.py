import asyncio

class _grove__ear_heart_rate:
    def __init__(self):
        self.keys = ['vcc', 'gnd', 'signal']
        self.required_keys = ['vcc', 'gnd']
        self.display_io_names = {'vcc': 'vcc', 'gnd': 'gnd', 'signal': 'signal'}
        self.interval = 5
        self.duration = 2.5 * 1000

    @staticmethod
    def info():
        return {'name': 'Grove_EarHeartRate'}

    def wired(self, obniz):
        self.obniz = obniz
        obniz.set_vcc_gnd(*[self.params.vcc, self.params.gnd, '5v'])

    def start(self, callback):
        self.obniz.logic_analyzer.start(*[{'io': self.params.signal, 'interval': self.interval, 'duration': self.duration}])
        self.obniz.logic_analyzer.onmeasured = # TODO: ArrowFunctionExpression was here

    def get_wait(self):
        return await# TODO: ArrowFunctionExpression was here