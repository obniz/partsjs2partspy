from attrdict import AttrDefault

class Solenoid:
    def __init__(self):
        self.keys = ['gnd', 'signal']
        self.required_keys = ['signal']

    @staticmethod
    def info():
        return AttrDefault(bool, {'name': 'Solenoid'})

    def wired(self, obniz):
        self.obniz = obniz
        if obniz.is_valid_io(*[self.params.gnd]):
            self.io_gnd = obniz.get_io(*[self.params.gnd])
            self.io_gnd.output(*[False])
        self.io_signal = obniz.get_io(*[self.params.signal])
        self.io_signal.output(*[False])

    def on(self):
        self.io_signal.output(*[True])

    def off(self):
        self.io_signal.output(*[False])

    def click(self, time_msec):
        self.on()
        if type(time_msec) != 'number':
            time_msec = 100
        self.obniz.wait(*[time_msec])
        self.off()

    def double_click(self, time_msec):
        if type(time_msec) != 'number':
            time_msec = 100
        self.click(*[time_msec])
        self.obniz.wait(*[time_msec])
        self.click(*[time_msec])