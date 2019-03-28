from attrdict import AttrDefault

class IRModule:
    def __init__(self):
        self.keys = ['recv', 'vcc', 'send', 'gnd']
        self.required_keys = ['recv', 'send']

    @staticmethod
    def info():
        return AttrDefault(bool, {'name': 'IRModule'})

    def wired(self, obniz):
        self.obniz = obniz
        obniz.set_vcc_gnd(*[self.params.vcc, self.params.gnd, '5v'])
        if not obniz.is_valid_io(*[self.params.recv]):
            raise Exception('recv is not valid io')
        if not obniz.is_valid_io(*[self.params.send]):
            raise Exception('send is not valid io')
        self.sensor = obniz.wired(*['IRSensor', AttrDefault(bool, {'output': self.params.recv})])
        self.set_getter_setter(*['sensor', 'duration'])
        self.set_getter_setter(*['sensor', 'dataInverted'])
        self.set_getter_setter(*['sensor', 'cutTail'])
        self.set_getter_setter(*['sensor', 'output_pullup'])
        self.set_getter_setter(*['sensor', 'ondetect'])
        self.led = obniz.wired(*['InfraredLED', AttrDefault(bool, {'anode': self.params.send})])

    def send(self, arr):
        self.led.send(*[arr])

    def start(self, callback):
        self.sensor.start(*[callback])

    def data_symbol_length(self):
        return self.sensor.data_symbol_length

    def data_symbol_length(self, x):
        self.sensor.data_symbol_length = x
        self.led.data_symbol_length = x

    def set_getter_setter(self, parts_name, var_name):
        def get():
            return self[partsName][varName]

        setattr(self, var_name, get)
        def set():
            self[partsName][varName] = x

        setattr(self, var_name, set)