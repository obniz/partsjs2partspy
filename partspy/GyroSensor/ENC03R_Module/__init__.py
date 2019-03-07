import asyncio

class _enc03_r__module:
    def __init__(self):
        self.keys = ['vcc', 'out1', 'out2', 'gnd']
        self.required = ['out1', 'out2']
        self._sens = 0.00067

    @staticmethod
    def info():
        return {'name': 'ENC03R_Module'}

    def wired(self, obniz):
        self.obniz = obniz
        obniz.set_vcc_gnd(*[self.params.vcc, self.params.gnd, '5v'])
        self.ad0 = obniz.get_ad(*[self.params.out1])
        self.ad1 = obniz.get_ad(*[self.params.out2])
        self.ad0.start(*[# TODO: ArrowFunctionExpression was here])
        self.ad1.start(*[# TODO: ArrowFunctionExpression was here])

    def get1_wait(self):
        return await# TODO: ArrowFunctionExpression was here

    def get2_wait(self):
        return await# TODO: ArrowFunctionExpression was here