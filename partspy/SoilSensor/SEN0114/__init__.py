import asyncio

class SEN0114:
    def __init__(self):
        self.keys = ['vcc', 'output', 'gnd']
        self.required_keys = ['output']

    @staticmethod
    def info():
        return {'name': 'SEN0114'}

    def wired(self, obniz):
        self.obniz = obniz
        self.obniz.set_vcc_gnd(*[self.params.vcc, self.params.gnd, '5v'])
        self.ad = obniz.get_ad(*[self.params.output])
        self.ad.start(*[# TODO: ArrowFunctionExpression was here])

    async def get_humidity_wait(self):
        self.value = await self.ad.get_wait()
        return self.value