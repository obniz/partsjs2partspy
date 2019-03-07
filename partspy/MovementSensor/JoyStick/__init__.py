import asyncio

class _joy_stick:
    def __init__(self):
        self.keys = ['sw', 'y', 'x', 'vcc', 'gnd', 'i2c']
        self.required_keys = ['sw', 'y', 'x']
        self.pins = self.keys or ['sw', 'y', 'x', 'vcc', 'gnd']
        self.pinname = {'sw': 'sw12'}
        self.short_name = 'joyS'

    @staticmethod
    def info():
        return {'name': 'JoyStick'}

    def wired(self, obniz):
        self.obniz = obniz
        obniz.set_vcc_gnd(*[self.params.vcc, self.params.gnd, '5v'])
        self.io_sig_sw = obniz.get_io(*[self.params.sw])
        self.ad_x = obniz.get_ad(*[self.params.x])
        self.ad_y = obniz.get_ad(*[self.params.y])
        self.io_sig_sw.pull(*['5v'])
        self = self
        self.ad_x.start(*[lambda value: self.position_x = value / 5.0])
        self.ad_y.start(*[lambda value: self.position_y = value / 5.0])
        self.io_sig_sw.input(*[lambda value: self.is_pressed = value == False])

    async def is_pressed_wait(self):
        ret = await self.io_sig_sw.input_wait()
        return ret == False

    async def get_xwait(self):
        value = await self.ad_x.get_wait()
        self.position_x = value / 5.0
        return self.position_x * 2 - 1

    async def get_ywait(self):
        value = await self.ad_y.get_wait()
        self.position_y = value / 5.0
        return self.position_y * 2 - 1