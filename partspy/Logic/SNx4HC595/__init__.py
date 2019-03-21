class _snx4_hc595:
    def __init__(self):
        self.keys = ['gnd', 'vcc', 'ser', 'srclk', 'rclk', 'oe', 'srclr', 'io_num', 'enabled']
        self.required_keys = ['ser', 'srclk', 'rclk']
        self.auto_flash = True

    @staticmethod
    def info():
        return {'name': 'SNx4HC595'}

    def wired(self, obniz):
        self.obniz = obniz
        self.io_ser = self.obniz.get_io(*[self.params.ser])
        self.io_srclk = self.obniz.get_io(*[self.params.srclk])
        self.io_rclk = self.obniz.get_io(*[self.params.rclk])
        self.io_ser.output(*[False])
        self.io_srclk.output(*[False])
        self.io_rclk.output(*[False])
        self.obniz.set_vcc_gnd(*[self.params.vcc, self.params.gnd, '5v'])
        if self.obniz.is_valid_io(*[self.params.srclr]):
            self.io_srclr = self.obniz.get_io(*[self.params.srclr])
            self.io_srclr.output(*[True])
        if self.obniz.is_valid_io(*[self.params.oe]):
            self.io_oe = self.obniz.get_io(*[self.params.oe])
            self.io_oe.output(*[True])
        if self.obniz.is_valid_io(*[self.params.vcc]) or self.obniz.is_valid_io(*[self.params.gnd]):
            self.obniz.wait(*[100])
        if type(self.params.io_num) != 'number':
            self.params.io_num = 8
        self.io_num(*[self.params.io_num])
        if type(self.params.enabled) != 'boolean':
            self.params.enabled = True
        if self.io_oe and self.params.enabled:
            self.io_oe.output(*[False])

    def io_num(self, num):
        class _snx4_hc595__io:
            def __init__(self, chip, id):
                self.chip = chip
                self.id = id
                self.value = 0

            def output(self, value):
                self.chip.output(*[self.id, value])


        if type(num) == 'number' and self._io_num != num:
            self._io_num = num
            self.io = []
            for i in range(0, num, 1):
                self.io.push(*[_snx4_hc595__io(*[self, i])])
            self.flush()
        else:
            raise Exception('io num should be a number')

    def is_valid_io(self, io):
        return type(io) == 'number' and io >= 0 and io < self._io_num

    def get_io(self, io):
        if not self.is_valid_io(*[io]):
            raise Exception(str('io ' + str(io)) + ' is not valid io')
        return self.io[io]

    def output(self, id, value):
        value = value == True
        self.io[id].value = value
        if self.auto_flash:
            self.flush()

    def onece(self, operation):
        if type(operation) != 'function':
            raise Exception('please provide function')
        lastValue = self.auto_flash
        self.auto_flash = False
        operation()
        self.flush()
        self.auto_flash = last_value

    def set_enable(self, enable):
        if not self.io_oe and enable == False:
            raise Exception('pin "oe" is not specified')
        self.io_oe.output(*[not enable])

    def flush(self):
        self.io_rclk.output(*[False])
        for i in range(self.io.length - 1, 0 - 1, -1):
            self.io_ser.output(*[self.io[i].value])
            self.io_srclk.output(*[True])
            self.io_srclk.output(*[False])
        self.io_rclk.output(*[True])