class _pca9685:
    def __init__(self):
        self.keys = ['gnd', 'vcc', 'scl', 'sda', 'oe', 'i2c', 'enabled', 'address', 'drive']
        self.required_keys = []
        self.address = 0x40
        self._commands = {'_mode1': 0x00, '_mode2': 0x01, '_subadr1': 0x02, '_subadr2': 0x03, '_subadr3': 0x04, '_prescale': 0xfe, '_led0__on__l': 0x06, '_all__led__on__l': 0xfa, 'bits': {'_allcall': 0x01, '_sleep__enable': 0x10, '_auto__increment__enabled': 0x20, '_restart': 0x80, '_outdrv': 0x04, '_invrt': 0x10}}
        self._regs = [0] * 1
        self.pwm_num = 16
        self.pwms = []
        self._prepare_pwm(*[self.pwm_num])

    @staticmethod
    def info():
        return {'name': 'PCA9685'}

    def wired(self, obniz):
        self.obniz = obniz
        if obniz.is_valid_io(*[self.params.oe]):
            self.io_oe = obniz.get_io(*[self.params.oe])
        self.obniz.set_vcc_gnd(*[self.params.vcc, self.params.gnd, '5v'])
        if type(self.params.address) == 'number':
            self.address = self.params.address
        self.params.clock = self.params.clock or 400 * 1000
        self.params.mode = self.params.mode or 'master'
        self.params.pull = self.params.pull or '5v'
        self.i2c = obniz.get_i2_cwith_config(*[self.params])
        if self.obniz.is_valid_io(*[self.params.srclr]):
            self.io_srclr = self.obniz.get_io(*[self.params.srclr])
            self.io_srclr.output(*[True])
        if type(self.params.enabled) != 'boolean':
            self.params.enabled = True
        if self.io_oe and self.params.enabled:
            self.io_oe.output(*[False])
        if self.params.drive == 'open-drain':
            self.i2c.write(*[self.address, [self._commands._mode2, self._commands.bits._outdrv]])
        mode1 = self._commands.bits._auto__increment__enabled
        mode1 = mode1 and ~self._commands.bits._sleep__enable
        self.i2c.write(*[self.address, [self._commands._mode1, mode1]])
        self.i2c.write(*[self.address, [self._commands._mode1, mode1 or self._commands.bits._restart]])
        self._regs[self._commands._mode1] = mode1
        obniz.wait(*[10])

    def _prepare_pwm(self, num):
        class _pca9685__pwm:
            def __init__(self, chip, id):
                self.chip = chip
                self.id = id
                self.value = 0
                self.state = }

            def freq(self, frequency):
                self.chip.freq(*[frequency])

            def pulse(self, value):
                self.chip.pulse(*[self.id, value])

            def duty(self, value):
                self.chip.duty(*[self.id, value])


        # TODO: failed to generate FOR statement

    def is_valid_pwm(self, id):
        return type(id) == 'number' and id >= 0 and id < self.pwm_num

    def get_pwm(self, id):
        if not self.is_valid_pwm(*[id]):
            raise Exception('pwm ' + id + ' is not valid pwm')
        return self.pwms[id]

    def freq(self, frequency):
        if type(frequency) != 'number':
            return
        if frequency < 24 or 1526 < frequency:
            raise Exception('freq must be within 24-1526 hz')
        if self._freq == frequency:
            return
        prescaleval = 25000000.0
        prescaleval /= 4096.0
        prescaleval /= frequency * 0.9
        prescaleval -= 1.0
        prescale = parse_int(*[_math.floor(*[prescaleval + 0.5])])
        mode1 = self._regs[self._commands._mode1]
        self.i2c.write(*[self.address, [self._commands._mode1, mode1 and 0x7f or self._commands.bits._sleep__enable]])
        self.i2c.write(*[self.address, [self._commands._prescale, prescale]])
        self.i2c.write(*[self.address, [self._commands._mode1, mode1]])
        self.obniz.wait(*[5])
        self._freq = frequency
        # TODO: failed to generate FOR statement

    def pulse(self, id, pulse_width):
        if type(self._freq) != 'number' or self._freq <= 0:
            raise Exception('please provide freq first.')
        self.duty(*[id, pulse_width / 1000.0 / 1.0 / self._freq * 100])

    def duty(self, id, duty):
        duty *= 1.0
        if type(self._freq) != 'number' or self._freq <= 0:
            raise Exception('please provide freq first.')
        if type(duty) != 'number':
            raise Exception('please provide duty in number')
        if duty < 0:
            duty = 0
        if duty > 100:
            duty = 100
        self.get_pwm(*[id]).state.duty = duty
        self.write_single_onoff(*[id, 0, duty / 100.0 * 4095])

    def write_single_onoff(self, id, on, off):
        self.i2c.write(*[self.address, [self._commands._led0__on__l + 4 * id, on and 0xff, on >> 8, off and 0xff, off >> 8]])

    def set_enable(self, enable):
        if not self.io_oe and enable == False:
            raise Exception('pin "oe" is not specified')
        self.io_oe.output(*[not enable])