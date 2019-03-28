from attrdict import AttrDefault

import asyncio

class HCSR04:
    def __init__(self):
        self.keys = ['vcc', 'trigger', 'echo', 'gnd']
        self.required_keys = ['vcc', 'trigger', 'echo']
        self._unit = 'mm'
        self.reset_alltime = False
        self.temp = 15

    @staticmethod
    def info():
        return AttrDefault(bool, {'name': 'HC-SR04'})

    def wired(self, obniz):
        self.obniz = obniz
        obniz.set_vcc_gnd(*[null, self.params.gnd, '5v'])
        self.vcc_io = obniz.get_io(*[self.params.vcc])
        self.trigger = self.params.trigger
        self.echo = self.params.echo
        self.vcc_io.drive(*['5v'])
        self.vcc_io.output(*[True])
        self.obniz.wait(*[100])

    def measure(self, callback):
        self = self
        self.obniz.measure.echo(*[AttrDefault(bool, {'io_pulse': self.trigger, 'io_echo': self.echo, 'pulse': 'positive', 'pulse_width': 0.011, 'measure_edges': 3, 'timeout': 10 / 340 * 1000, 'callback': # TODO: ArrowFunctionExpression was here})])

    async def measure_wait(self):
        return await# TODO: ArrowFunctionExpression was here

    def unit(self, unit):
        if unit == 'mm':
            self._unit = 'mm'
        elif unit == 'inch':
            self._unit = 'inch'
        else:
            raise Exception('HCSR04: unknown unit ' + str(unit))