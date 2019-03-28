from attrdict import AttrDefault

import asyncio

class Button:
    def __init__(self):
        self.keys = ['signal', 'gnd']
        self.required = ['signal']
        self.on_change_for_state_wait = # TODO: failed to generate Function Expression

    @staticmethod
    def info():
        return AttrDefault(bool, {'name': 'Button'})

    def wired(self, obniz):
        self.io_signal = obniz.get_io(*[self.params.signal])
        if obniz.is_valid_io(*[self.params.gnd]):
            self.io_supply = obniz.get_io(*[self.params.gnd])
            self.io_supply.output(*[False])
        self.io_signal.pull(*['5v'])
        self = self
        self.io_signal.input(*[lambda value: self.is_pressed = value == False])

    async def is_pressed_wait(self):
        ret = await self.io_signal.input_wait()
        return ret == False

    def state_wait(self, is_pressed):
        return await# TODO: ArrowFunctionExpression was here