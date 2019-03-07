import asyncio

class hx711:
    def __init__(self):
        self.keys = ['vcc', 'gnd', 'sck', 'dout']
        self.required_keys = ['sck', 'dout']
        self.offset = 0
        self.scale = 1

    @staticmethod
    def info():
        return {'name': 'hx711'}

    def wired(self, obniz):
        self.obniz = obniz
        self.spi = obniz.get_free_spi()
        obniz.set_vcc_gnd(*[self.params.vcc, self.params.gnd, '5v'])
        ioKeys = ['clk', 'dout']
        for key in io_keys:
            if self.params[key] and not self.obniz.is_valid_io(*[self.params[key]]):
                raise Exception("spi start param '" + key + "' are to be valid io no")
        self.sck = obniz.get_io(*[self.params.sck])
        self.dout = obniz.get_io(*[self.params.dout])
        self.sck.output(*[True])

    async def read_wait(self):
        self.sck.output(*[False])
        self.spi.start(*[{'mode': 'master', 'clk': self.params.sck, 'miso': self.params.dout, 'frequency': 66 * 1000}])
        ret = await self.spi.write_wait(*[[0, 0, 0]])
        self.spi.end(*[True])
        self.sck.output(*[False])
        flag = 1 if ret[0] and 0x80 == 0 else -1
        return flag * ret[0] and 0x7f << 16 + ret[1] << 8 + ret[2] << 0

    async def read_average_wait(self, times):
        results = []
        # TODO: failed to generate FOR statement
        return results.reduce(*[lambda prev, current, i: prev + current, 0]) / results.length

    def power_down(self):
        self.sck.output(*[True])

    def power_up(self):
        self.sck.output(*[False])

    async def zero_adjust(self, times):
        times = parse_int(*[times]) or 1
        self.offset = await self.read_average_wait(*[times])

    async def get_value_wait(self, times):
        times = parse_int(*[times]) or 1
        val = await self.read_average_wait(*[times])
        return val - self.offset / self.scale