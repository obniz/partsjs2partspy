import asyncio

class FSR40X:
    def __init__(self):
        self.keys = ['pin0', 'pin1']
        self.required_keys = ['pin0', 'pin1']

    @staticmethod
    def info():
        return {'name': 'FSR40X'}

    def wired(self, obniz):
        self.obniz = obniz
        self.io_pwr = obniz.get_io(*[self.params.pin0])
        self.ad = obniz.get_ad(*[self.params.pin1])
        self.io_pwr.drive(*['5v'])
        self.io_pwr.output(*[True])
        self = self
        self.ad.start(*[# TODO: failed to generate Function Expression])

    async def get_wait(self):
        value = await self.ad.get_wait()
        pressure = value * 100
        self.press = pressure
        return self.press