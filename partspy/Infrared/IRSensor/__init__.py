class _irsensor:
    def __init__(self):
        self.keys = ['output', 'vcc', 'gnd']
        self.required_keys = ['output']
        self.data_symbol_length = 0.07
        self.duration = 500
        self.data_inverted = True
        self.trigger_sample_count = 16
        self.cut_tail = False
        self.output_pullup = True

    @staticmethod
    def info():
        return {'name': 'IRSensor'}

    def wired(self, obniz):
        self.obniz = obniz
        obniz.set_vcc_gnd(*[self.params.vcc, self.params.gnd, '5v'])
        if not obniz.is_valid_io(*[self.params.output]):
            raise Exception('output is not valid io')

    def start(self, callback):
        self.ondetect = callback
        if self.output_pullup:
            self.obniz.get_io(*[self.params.output]).pull(*['5v'])
        self.obniz.logic_analyzer.start(*[{'io': self.params.output, 'interval': self.data_symbol_length, 'duration': self.duration, 'trigger_value': False if self.data_inverted else True, 'trigger_value_samples': self.trigger_sample_count}])
        self.obniz.logic_analyzer.onmeasured = # TODO: ArrowFunctionExpression was here