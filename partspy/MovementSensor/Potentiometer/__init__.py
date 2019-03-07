class _potentiometer:
    def __init__(self):
        self.keys = ['pin0', 'pin1', 'pin2']
        self.reuired_keys = ['pin0', 'pin1', 'pin2']
        self.vcc_voltage = 5.0

    @staticmethod
    def info():
        return {'name': 'Potentiometer'}

    def wired(self, obniz):
        self.obniz.set_vcc_gnd(*[self.params.pin0, self.params.pin2, '5v'])
        self.ad = obniz.get_ad(*[self.params.pin1])
        self = self
        obniz.get_ad(*[self.params.pin0]).start(*[lambda value: self.vcc_voltage = value])
        self.ad.start(*[lambda value: self.position = value / self.vcc_voltage])