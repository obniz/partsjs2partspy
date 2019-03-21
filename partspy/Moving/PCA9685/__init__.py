class PCA9685:
    def __init__(self):
        self.keys = ['gnd', 'vcc', 'scl', 'sda', 'oe', 'i2c', 'enabled', 'address', 'drive']
        self.required_keys = []
        self.address = 0x40
        self._commands = {'MODE1': 0x00, 'MODE2': 0x01, 'SUBADR1': 0x02, 'SUBADR2': 0x03, 'SUBADR3': 0x04, 'PRESCALE': 0xfe, 'LED0_ON_L': 0x06, 'ALL_LED_ON_L': 0xfa, 'bits': {'ALLCALL': 0x01, 'SLEEP_ENABLE': 0x10, 'AUTO_INCREMENT_ENABLED': 0x20, 'RESTART': 0x80, 'OUTDRV': 0x04, 'INVRT': 0x10}}
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
            self.i2c.write(*[self.address, [self._commands.MODE2, self._commands.bits.OUTDRV]])
        mode1 = self._commands.bits.AUTO_INCREMENT_ENABLED
        mode1 = mode1 and ~self._commands.bits.SLEEP_ENABLE
        self.i2c.write(*[self.address, [self._commands.MODE1, mode1]])
        self.i2c.write(*[self.address, [self._commands.MODE1, mode1 or self._commands.bits.RESTART]])
        self._regs[self._commands.MODE1] = mode1
        obniz.wait(*[10])

    def _prepare_pwm(self, num):
        class PCA9685_PWM:
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


        for i in range(0, num, 1):
            self.pwms.push(*[PCA9685_PWM(*[self, i])])

    def is_valid_pwm(self, id):
        return type(id) == 'number' and id >= 0 and id < self.pwm_num

    def get_pwm(self, id):
        if not self.is_valid_pwm(*[id]):
            raise Exception(str('pwm ' + str(id)) + ' is not valid pwm')
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
        mode1 = self._regs[self._commands.MODE1]
        self.i2c.write(*[self.address, [self._commands.MODE1, mode1 and 0x7f or self._commands.bits.SLEEP_ENABLE]])
        self.i2c.write(*[self.address, [self._commands.PRESCALE, prescale]])
        self.i2c.write(*[self.address, [self._commands.MODE1, mode1]])
        self.obniz.wait(*[5])
        self._freq = frequency
        for i in range(0, self.pwms.length, 1):
            self.pwms[i].state.freq = self._freq

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
        self.i2c.write(*[self.address, [self._commands.LED0_ON_L + 4 * id, on and 0xff, on >> 8, off and 0xff, off >> 8]])

    def set_enable(self, enable):
        if not self.io_oe and enable == False:
            raise Exception('pin "oe" is not specified')
        self.io_oe.output(*[not enable])