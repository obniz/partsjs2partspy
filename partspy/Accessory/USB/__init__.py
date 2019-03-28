from attrdict import AttrDefault

class USB:
    def __init__(self):
        self.keys = ['vcc', 'gnd']
        self.required_keys = ['vcc', 'gnd']
        self.display_io_names = AttrDefault(bool, {'vcc': 'vcc', 'gnd': 'gnd'})

    @staticmethod
    def info():
        return AttrDefault(bool, {'name': 'USB'})

    def wired(self, obniz):
        self.obniz = obniz
        self.io_vdd = obniz.get_io(*[self.params.vcc])
        self.io_gnd = obniz.get_io(*[self.params.gnd])
        self.io_gnd.output(*[False])

    def on(self):
        self.io_vdd.output(*[True])

    def off(self):
        self.io_vdd.output(*[False])