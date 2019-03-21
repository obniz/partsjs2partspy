import asyncio

class _jpeg_serial_cam:
    def __init__(self):
        self.keys = ['vcc', 'cam_tx', 'cam_rx', 'gnd']
        self.required_keys = ['cam_tx', 'cam_rx']
        self.io_keys = self.keys
        self.display_name = 'Jcam'
        self.display_io_names = {'cam_tx': 'camTx', 'cam_rx': 'camRx'}

    @staticmethod
    def info():
        return {'name': 'JpegSerialCam'}

    def wired(self, obniz):
        self.obniz = obniz
        self.obniz.set_vcc_gnd(*[self.params.vcc, self.params.gnd, '5v'])
        self.my_tx = self.params.cam_rx
        self.my_rx = self.params.cam_tx
        self.obniz.get_io(*[self.my_tx]).drive(*['3v'])
        self.uart = self.obniz.get_free_uart()

    async def _drain_until(self, uart, search, recv):
        if not recv:
            recv = []
        while True:
            readed = uart.read_bytes()
            recv = recv.concat(*[readed])
            tail = self._seek_tail(*[search, recv])
            if tail >= 0:
                recv.splice(*[0, tail])
                return recv
            await self.obniz.wait(*[10])

    def _seek_tail(self, search, src):
        f = 0
        for i in range(0, src.length, 1):
            if src[i] == search[f]:

                if f == search.length:
                    return i + 1
            else:
                f = 0
        return -1

    def array_to_base64(self, array):
        return _buffer.from(*[array]).to_string(*['base64'])

    async def start_wait(self, obj):
        if not obj:
            obj = }
        self.uart.start(*[{'tx': self.my_tx, 'rx': self.my_rx, 'baud': obj.baud or 38400}])
        self.obniz.display.set_pin_name(*[self.my_tx, 'JpegSerialCam', 'camRx'])
        self.obniz.display.set_pin_name(*[self.my_rx, 'JpegSerialCam', 'camTx'])
        await self.obniz.wait(*[2500])

    async def resetwait(self):
        self.uart.send(*[[0x56, 0x00, 0x26, 0x00]])
        await self._drain_until(*[self.uart, [0x76, 0x00, 0x26, 0x00]])
        await self.obniz.wait(*[2500])

    async def set_size_wait(self, resolution):
        val = None
        if resolution == '640x480':
            val = 0x00
        elif resolution == '320x240':
            val = 0x11
        elif resolution == '160x120':
            val = 0x22
        else:
            raise Exception('unsupported size')
        self.uart.send(*[[0x56, 0x00, 0x31, 0x05, 0x04, 0x01, 0x00, 0x19, val]])
        await self._drain_until(*[self.uart, [0x76, 0x00, 0x31, 0x00]])
        await self.resetwait()

    async def set_compressibility_wait(self, compress):
        val = _math.floor(*[compress / 100 * 0xff])
        self.uart.send(*[[0x56, 0x00, 0x31, 0x05, 0x01, 0x01, 0x12, 0x04, val]])
        await self._drain_until(*[self.uart, [0x76, 0x00, 0x31, 0x00]])
        await self.resetwait()

    async def set_baud_wait(self, baud):
        val = None
        if baud==9600:
            val = [0xae, 0xc8]
        elif baud==19200:
            val = [0x56, 0xe4]
        elif baud==38400:
            val = [0x2a, 0xf2]
        elif baud==57600:
            val = [0x1c, 0x4c]
        elif baud==115200:
            val = [0x0d, 0xa6]
        else:
            raise Exception('invalid baud rate')
        self.uart.send(*[[0x56, 0x00, 0x31, 0x06, 0x04, 0x02, 0x00, 0x08, val[0], val[1]]])
        await self._drain_until(*[self.uart, [0x76, 0x00, 0x31, 0x00]])
        await self.startwait(*[{'baud': baud}])

    async def take_wait(self):
        uart = self.uart
        uart.send(*[[0x56, 0x00, 0x36, 0x01, 0x02]])
        await self._drain_until(*[uart, [0x76, 0x00, 0x36, 0x00, 0x00]])
        uart.send(*[[0x56, 0x00, 0x36, 0x01, 0x00]])
        await self._drain_until(*[uart, [0x76, 0x00, 0x36, 0x00, 0x00]])
        uart.send(*[[0x56, 0x00, 0x34, 0x01, 0x00]])
        recv = await self._drain_until(*[uart, [0x76, 0x00, 0x34, 0x00, 0x04, 0x00, 0x00]])
        XX = None
        YY = None
        while True:
            readed = uart.read_bytes()
            recv = recv.concat(*[readed])
            if recv.length >= 2:
                XX = recv[0]
                YY = recv[1]
                break
            await self.obniz.wait(*[1000])
        databytes = XX * 256 + YY
        uart.send(*[[0x56, 0x00, 0x32, 0x0c, 0x00, 0x0a, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, XX, YY, 0x00, 0xff]])
        recv = await self._drain_until(*[uart, [0x76, 0x00, 0x32, 0x00, 0x00]])
        while True:
            readed = uart.read_bytes()
            recv = recv.concat(*[readed])
            if recv.length >= databytes:
                break
            await self.obniz.wait(*[10])
        recv = recv.splice(*[0, databytes])
        recv = recv.concat(*[[0xff, 0xd9]])
        return recv