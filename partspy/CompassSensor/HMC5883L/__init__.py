import asyncio

class _hmc5883_l:
    def __init__(self):
        self.keys = ['gnd', 'sda', 'scl', 'i2c']
        self.address = }
        self.address.device = 0x1e
        self.address.reset = [0x02, 0x00]
        self.address.x_msb = [0x03]

    @staticmethod
    def info():
        return {'name': 'HMC5883L'}

    def wired(self, obniz):
        self.obniz = obniz
        obniz.set_vcc_gnd(*[null, self.params.gnd, '3v'])
        self.params.clock = 100000
        self.params.pull = '3v'
        self.params.mode = 'master'
        self.i2c = obniz.get_i2_cwith_config(*[self.params])
        self.obniz.wait(*[500])

    def init(self):
        self.i2c.write(*[self.address.device, self.address.reset])
        self.obniz.wait(*[500])

    async def get(self):
        self.i2c.write(*[self.address.device, self.address.x_msb])
        readed = await self.i2c.read_wait(*[self.address.device, 2 * 3])
        obj = }
        keys = ['x', 'y', 'z']
        # TODO: failed to generate FOR statement
        return obj