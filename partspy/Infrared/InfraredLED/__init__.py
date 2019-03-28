from attrdict import AttrDefault

class InfraredLED:
    def __init__(self):
        self.keys = ['anode', 'cathode']
        self.required_keys = ['anode']
        self.data_symbol_length = 0.07

    @staticmethod
    def info():
        return AttrDefault(bool, {'name': 'InfraredLED'})

    def wired(self, obniz):
        self.obniz = obniz
        if not self.obniz.is_valid_io(*[self.params.anode]):
            raise Exception('anode is not valid io')
        if self.params.cathode:
            if not self.obniz.is_valid_io(*[self.params.cathode]):
                raise Exception('cathode is not valid io')
            self.io_cathode = obniz.get_io(*[self.params.cathode])
            self.io_cathode.output(*[False])
        self.pwm = self.obniz.get_free_pwm()
        self.pwm.start(*[AttrDefault(bool, {'io': self.params.anode})])
        self.pwm.freq(*[38000])
        self.obniz.wait(*[150])

    def send(self, arr):
        if arr and arr.length > 0 and arr[(arr.length - 1)] == 1:
            arr.push(*[0])
        self.pwm.modulate(*['am', self.data_symbol_length, arr])