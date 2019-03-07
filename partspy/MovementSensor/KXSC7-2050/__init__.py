import asyncio

class _kxsc7_2050:
    def __init__(self):
        self.keys = ['x', 'y', 'z', 'vcc', 'gnd']
        self.required_keys = ['x', 'y', 'z']

    @staticmethod
    def info():
        return {'name': 'KXSC7-2050'}

    async def wired(self, obniz):
        self.obniz = obniz
        obniz.set_vcc_gnd(*[self.params.vcc, self.params.gnd, '3v'])
        self.ad_x = obniz.get_ad(*[self.params.x])
        self.ad_y = obniz.get_ad(*[self.params.y])
        self.ad_z = obniz.get_ad(*[self.params.z])
        await obniz.wait(*[500])
        ad = obniz.get_ad(*[self.params.vcc])
        pwrVoltage = await ad.get_wait()
        horizontalZ = await self.ad_z.get_wait()
        sensitivity = pwr_voltage / 5
        offsetVoltage = horizontal_z - sensitivity
        self = self
        self.ad_x.start(*[lambda value: self.gravity = value - offset_voltage / sensitivity])
        self.ad_y.start(*[lambda value: self.gravity = value - offset_voltage / sensitivity])
        self.ad_z.start(*[lambda value: self.gravity = value - offset_voltage / sensitivity])