class _speaker:
    def __init__(self, obniz):
        self.keys = ['signal', 'gnd']
        self.required_keys = ['gnd']

    @staticmethod
    def info():
        return {'name': 'Speaker'}

    def wired(self, obniz):
        self.obniz = obniz
        self.obniz.set_vcc_gnd(*[null, self.params.gnd, '5v'])
        self.pwm = obniz.get_free_pwm()
        self.pwm.start(*[{'io': self.params.signal}])

    def play(self, freq):
        if type(freq) != 'number':
            raise Exception('freq must be a number')
        freq = parse_int(*[freq])
        if freq > 0:
            self.pwm.freq(*[freq])
            self.pwm.pulse(*[1 / freq / 2 * 1000])
        else:
            self.pwm.pulse(*[0])

    def stop(self):
        self.play(*[0])