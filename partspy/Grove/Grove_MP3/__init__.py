from attrdict import AttrDefault

import asyncio

class Grove_MP3:
    def __init__(self):
        self.keys = ['vcc', 'gnd', 'mp3_rx', 'mp3_tx']
        self.required_keys = ['mp3_rx', 'mp3_tx']
        self.io_keys = self.keys
        self.display_name = 'MP3'
        self.display_io_names = AttrDefault(bool, {'mp3_rx': 'MP3Rx', 'mp3_tx': 'MP3Tx'})

    @staticmethod
    def info():
        return AttrDefault(bool, {'name': 'Grove_MP3'})

    def wired(self, obniz):
        self.obniz = obniz
        obniz.set_vcc_gnd(*[self.params.vcc, self.params.gnd, '5v'])
        self.my_tx = self.params.mp3_rx
        self.my_rx = self.params.mp3_tx
        self.uart = self.obniz.get_free_uart()

    async def init_wait(self, strage):
        self.uart.start(*[AttrDefault(bool, {'tx': self.my_tx, 'rx': self.my_rx, 'baud': 9600})])
        await self.obniz.wait(*[100])
        self.uart_send(*[0x0c, 0])
        await self.obniz.wait(*[500])
        self.uart_send(*[0x0b, 0])
        await self.obniz.wait(*[100])
        if strage:
            if strage == 'usb':
                self.uart_send(*[0x09, 1])
            elif strage == 'sd':
                self.uart_send(*[0x09, 2])
        else:
            self.uart_send(*[0x09, 2])
        await self.obniz.wait(*[200])

    def set_volume(self, vol):
        if vol >= 0 and vol <= 31:
            self.uart_send(*[0x06, vol])

    def vol_up(self):
        self.uart_send(*[0x04, 0])

    def vol_down(self):
        self.uart_send(*[0x05, 0])

    def play(self, track, folder):
        if folder:
            self.uart.send(*[[0x7e, 0xff, 0x06, 0x0f, 0x00, folder, track, 0xef]])
        else:
            self.uart_send(*[0x12, track])

    def stop(self):
        self.uart_send(*[0x16, 0])

    def pause(self):
        self.uart_send(*[0x0e, 0])

    def resume(self):
        self.uart_send(*[0x0d, 0])

    def next(self):
        self.uart_send(*[0x01, 0])

    def prev(self):
        self.uart_send(*[0x02, 0])

    def uart_send(self, command, param):
        paramM = param >> 8
        paramL = param and 0xff
        self.uart.send(*[[0x7e, 0xff, 0x06, command, 0x01, param_m, param_l, 0xef]])
        response = self.uart.read_bytes()
        return response