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
        # TODO: failed to generate FOR statement

    def brightness(self, val):
        self.write(*[[0x0a, val]])
        self.passing_commands()

    def preparevram(self, width, height):
        self.vram = []
        # TODO: failed to generate FOR statement

    def write(self, data):
        self.cs.output(*[False])
        self.spi.write(*[data])
        self.cs.output(*[True])

    def write_vram(self):
        # TODO: failed to generate FOR statement

    def clear(self):
        # TODO: failed to generate FOR statement

    def draw(self, ctx):
        imageData = ctx.get_image_data(*[0, 0, self.width, self.height])
        data = image_data.data
        # TODO: failed to generate FOR statement
        self.write_vram()