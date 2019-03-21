import asyncio

class _24LC256:
    def __init__(self):
        self.required_keys = ['address']
        self.keys = ['sda', 'scl', 'clock', 'pull', 'i2c', 'address']

    @staticmethod
    def info():
        return {'name': '24LC256'}

    def wired(self, obniz):
        self.params.mode = self.params.mode or 'master'
        self.params.clock = self.params.clock or 400 * 1000
        self.i2c = obniz.get_i2_cwith_config(*[self.params])

    def set(self, address, data):
        array = []
        array.push(*[address >> 8 and 0xff])
        array.push(*[address and 0xff])
        array.push.apply(*[array, data])
        self.i2c.write(*[0x50, array])
        self.obniz.wait(*[4 + 1])

    async def get_wait(self, address, length):
        array = []
        array.push(*[address >> 8 and 0xff])
        array.push(*[address and 0xff])
        self.i2c.write(*[0x50, array])
        return await self.i2c.read_wait(*[0x50, length])