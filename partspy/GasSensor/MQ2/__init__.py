from attrdict import AttrDefault

import asyncio

class MQ2:
    def __init__(self):
        self.keys = ['gnd', 'vcc', 'do', 'ao']
        self.required_keys = []
        self.onchangeanalog = undefined
        self.onchangedigital = undefined
        self.onexceedvoltage = undefined
        self.voltage_limit = undefined

    @staticmethod
    def info():
        return AttrDefault(bool, {'name': 'MQ2'})

    def wired(self, obniz):
        self.obniz = obniz
        self.vcc = self.params.vcc
        self.gnd = self.params.gnd
        if self.obniz.is_valid_io(*[self.params.ao]):
            self.ad = obniz.get_ad(*[self.params.ao])
            self.ad.start(*[# TODO: ArrowFunctionExpression was here])
        if self.obniz.is_valid_io(*[self.params.do]):
            self.do = obniz.get_io(*[self.params.do])
            self.do.input(*[# TODO: ArrowFunctionExpression was here])

    def start_heating(self):
        self.obniz.set_vcc_gnd(*[self.vcc, self.gnd, '5v'])

    def heat_wait(self, seconds):
        self.start_heating()
        if seconds > 0:
            seconds *= 1000
        else:
            seconds = 2 * 60 * 1000
        return await# TODO: ArrowFunctionExpression was here