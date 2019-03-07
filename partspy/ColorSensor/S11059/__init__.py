import asyncio

class _s11059:
    def __init__(self):
        self.keys = ['vcc', 'sda', 'scl', 'i2c', 'gnd']
        self.required_keys = []
        self.address = 0x2a
        self.reg_adrs = }
        self.reg_adrs.ctrl = 0x00
        self.reg_adrs.manual_timing = 0x01
        self.reg_adrs.sensor_red = 0x03

    @staticmethod
    def info():
        return {'name': 'S11059'}

    def wired(self, obniz):
        self.obniz = obniz
        obniz.set_vcc_gnd(*[self.params.vcc, self.params.gnd, '3v'])
        self.obniz.wait(*[100])
        self.params.clock = 100000
        self.params.pull = '3v'
        self.params.mode = 'master'
        self.i2c = obniz.get_i2_cwith_config(*[self.params])
        self.obniz.wait(*[100])

    def init(self, gain, int_time):
        self.i2c.write(*[self.address, [self.reg_adrs.ctrl, 0x80]])
        val = gain << 3 or int_time
        self.i2c.write(*[self.address, [self.reg_adrs.ctrl, val]])

    async def get_val(self):
        self.i2c.write(*[self.address, [self.reg_adrs.sensor_red]])
        ret = await self.i2c.read_wait(*[self.address, 8])
        level = [0, 0, 0, 0]
        level[0] = ret[0] << 8 or ret[1]
        level[1] = ret[2] << 8 or ret[3]
        level[2] = ret[4] << 8 or ret[5]
        level[3] = ret[6] << 8 or ret[7]
        return level