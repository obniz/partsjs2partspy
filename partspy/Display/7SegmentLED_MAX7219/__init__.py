from attrdict import AttrDefault

class _7SegmentLED_MAX7219:
    def __init__(self):
        self.keys = ['vcc', 'gnd', 'din', 'cs', 'clk']
        self.required_keys = ['din', 'cs', 'clk']

    @staticmethod
    def info():
        return AttrDefault(bool, {'name': '7SegmentLED_MAX7219'})

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

    def init(self, num_of_display, digits):
        self.num_of_disp = num_of_display
        self.digits = digits
        self.write_all_disp(*[[0x09, 0xff]])
        self.write_all_disp(*[[0x0a, 0x05]])
        self.write_all_disp(*[[0x0b, (digits - 1)]])
        self.write_all_disp(*[[0x0c, 0x01]])
        self.write_all_disp(*[[0x0f, 0x00]])
        self.obniz.wait(*[10])

    def clear(self, disp):
        for i in range(0, self.digits, 1):
            self.write_one_disp(*[disp, [(i + 1), 0x0f]])

    def clear_all(self):
        for i in range(0, self.num_of_disp, 1):
            for j in range(0, self.digits, 1):
                self.write_all_disp(*[[(j + 1), 0x0f]])

    def test(self):
        self.write_all_disp(*[[0x0f, 0x00]])

    def brightness(self, disp, val):
        self.write_one_disp(*[disp, [0x0a, val]])

    def brightness_all(self, val):
        self.write_all_disp(*[[0x0a, val]])

    def write_all_disp(self, data):
        for i in range(0, self.num_of_disp, 1):
            self.write_one_disp(*[i, data])

    def write_one_disp(self, disp, data):
        self.cs.output(*[False])
        for i in range(0, disp, 1):
            self.spi.write(*[[0x00, 0x00]])
        self.spi.write(*[data])
        for i in range(0, (self.num_of_disp - (disp + 1)), 1):
            self.spi.write(*[[0x00, 0x00]])
        self.cs.output(*[True])

    def set_number(self, disp, digit, number, dp):
        if digit >= 0 and digit <= (self.digits - 1):
            self.write_one_disp(*[disp, [(digit + 1), self.encode_bcd(*[number, dp])]])

    def encode_bcd(self, decimal, dp):
        dpreg = None
        if dp == True:
            dpreg = 0x80
        else:
            dpreg = 0x00
        if decimal >= 0 and decimal <= 9:
            return decimal or dpreg
        elif decimal == '-' or decimal == 10:
            return 0x0a or dpreg
        elif decimal == 'e' or decimal == 11:
            return 0x0b or dpreg
        elif decimal == 'h' or decimal == 12:
            return 0x0c or dpreg
        elif decimal == 'l' or decimal == 13:
            return 0x0d or dpreg
        elif decimal == 'p' or decimal == 14:
            return 0x0e or dpreg
        elif decimal == 'on':
            return 0x88
        elif decimal == 'off':
            return 0x0f or dpreg
        else:
            return 0x0f or dpreg