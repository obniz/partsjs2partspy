import asyncio

class _analog_templature_sensor:
    def __init__(self):
        self.keys = ['vcc', 'gnd', 'output']
        self.required_keys = ['output']
        self.drive = '5v'

    def wired(self, obniz):
        self.obniz = obniz
        obniz.set_vcc_gnd(*[self.params.vcc, self.params.gnd, self.drive])
        self.ad = obniz.get_ad(*[self.params.output])
        self.ad.start(*[lambda voltage: self.temp = self.calc(*[voltage])])

    async def get_wait(self):
        voltage = await self.ad.get_wait()
        self.temp = self.calc(*[voltage])
        return self.temp

    def onchange(self, temp):


    def calc(self, voltage):
        return 0