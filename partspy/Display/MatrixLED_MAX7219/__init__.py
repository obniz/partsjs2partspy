class _matrix_led__max7219:
    def __init__(self):
        self.keys = ['vcc', 'gnd', 'din', 'cs', 'clk']
        self.required_keys = ['din', 'cs', 'clk']

    @staticmethod
    def info():
        return {'name': 'MatrixLED_MAX7219'}

    def wired(self, obniz):
        self.cs = obniz.get_io(*[self.params.cs])
        if obniz.is_valid_io(*[self.params.vcc]):
            obniz.get_io(*[self.params.vcc]).output(*[True])
        if obniz.is_valid_io(*[self.params.gnd]):
            obniz.get_io(*[self.params.gnd]).output(*[False])
        self.params.frequency = self.params.frequency or 10 * 1000 * 1000
        self.params.mode = 'master'
        self.params.mosi = self.params.din
        self.params.drive = '3v'
        self.spi = self.obniz.get_spi_with_config(*[self.params])
        self.cs.output(*[True])
        self.cs.output(*[False])
        self.cs.output(*[True])

    def init(self, width, height):
        self.width = width
        self.height = height
        self.preparevram(*[width, height])
        self.init_module()

    def init_module(self):
        self.write(*[[0x09, 0x00]])
        self.write(*[[0x0a, 0x05]])
        self.write(*[[0x0b, 0x07]])
        self.write(*[[0x0c, 0x01]])
        self.write(*[[0x0f, 0x00]])
        self.passing_commands()
        self.obniz.wait(*[10])

    def test(self):
        self.write(*[[0x0f, 0x00]])
        self.passing_commands()

    def passing_commands(self):
        for i in range(8, self.width, 8):
            self.write(*[[0x00, 0x00]])

    def brightness(self, val):
        self.write(*[[0x0a, val]])
        self.passing_commands()

    def preparevram(self, width, height):
        self.vram = []
        for i in range(0, height, 1):
            dots = [0] * width / 8
            for ii in range(0, dots.length, 1):
                dots[ii] = 0x00
            self.vram.push(*[dots])

    def write(self, data):
        self.cs.output(*[False])
        self.spi.write(*[data])
        self.cs.output(*[True])

    def write_vram(self):
        for line_num in range(0, self.height, 1):
            addr = line_num + 1
            line = self.vram[line_num]
            data = []
            for col in range(0, line.length, 1):
                data.push(*[addr])
                data.push(*[line[col]])
            self.write(*[data])

    def clear(self):
        for line_num in range(0, self.height, 1):
            line = self.vram[line_num]
            for col in range(0, line.length, 1):
                self.vram[line_num][col] = 0x00
            self.write_vram()

    def draw(self, ctx):
        imageData = ctx.get_image_data(*[0, 0, self.width, self.height])
        data = image_data.data
        for i in range(0, data.length, 4):
            brightness = 0.34 * data[i] + 0.5 * data[i + 1] + 0.16 * data[i + 2]
            index = parse_int(*[i / 4])
            line = parse_int(*[index / self.width])
            col = parse_int(*[index - line * self.width / 8])
            bits = parse_int(*[index - line * self.width]) % 8
            if bits == 0:
                self.vram[line][col] = 0x00
            if brightness > 0x7f:
                self.vram[line][col] |= 0x80 >> bits
        self.write_vram()