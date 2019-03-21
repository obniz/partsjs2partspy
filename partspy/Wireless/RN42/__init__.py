class RN42:
    def __init__(self):
        self.keys = ['tx', 'rx', 'gnd']
        self.required_keys = ['tx', 'rx']

    @staticmethod
    def info():
        return {'name': 'RN42'}

    def wired(self, obniz):
        if obniz.is_valid_io(*[self.params.gnd]):
            obniz.get_io(*[self.params.gnd]).output(*[False])
        self.uart = obniz.get_free_uart()
        self.uart.start(*[{'tx': self.params.tx, 'rx': self.params.rx, 'baud': 115200, 'drive': '3v'}])
        self = self
        self.uart.onreceive = # TODO: ArrowFunctionExpression was here

    def send(self, data):
        self.uart.send(*[data])

    def send_command(self, data):
        self.uart.send(*[str(data) + '\n'])
        self.obniz.wait(*[100])

    def enter_command_mode(self):
        self.send(*['$$$'])
        self.obniz.wait(*[100])

    def config(self, json):
        self.enter_command_mode()
        if type(json) != 'object':
            return
        self.send_command(*[''])
        if json.master_slave:
            self.config_masterslave(*[json.master_slave])
        if json.auth:
            self.config_auth(*[json.auth])
        if json.hid_flag:
            self.config__hidflag(*[json.hid_flag])
        if json.profile:
            self.config_profile(*[json.profile])
        if json.power:
            self.config_power(*[json.power])
        if json.display_name:
            self.config_display_name(*[json.display_name])
        self.config_reboot()

    def config_reboot(self):
        self.send_command(*['R,1'])

    def config_masterslave(self, mode):
        val = -1
        if type(mode) == 'number':
            val = mode
        elif type(mode) == 'string':
            modes = ['slave', 'master', 'trigger', 'auto-connect-master', 'auto-connect-dtr', 'auto-connect-any', 'pairing']
            for i in range(0, modes.length, 1):
                if modes[i] == mode:
                    val = i
                    break
        if val == -1:
            return
        self.send_command(*['SM,' + str(val)])

    def config_display_name(self, name):
        self.send_command(*['SN,' + str(name)])

    def config__hidflag(self, flag):
        self.send_command(*['SH,' + str(flag)])

    def config_profile(self, mode):
        val = -1
        if type(mode) == 'number':
            val = mode
        elif type(mode) == 'string':
            modes = ['SPP', 'DUN-DCE', 'DUN-DTE', 'MDM-SPP', 'SPP-DUN-DCE', 'APL', 'HID']
            for i in range(0, modes.length, 1):
                if modes[i] == mode:
                    val = i
                    break
        if val == -1:
            return
        self.send_command(*['S~,' + str(val)])

    def config_revert_localecho(self):
        self.send_command(*['+'])

    def config_auth(self, mode):
        val = -1
        if type(mode) == 'number':
            val = mode
        elif type(mode) == 'string':
            modes = ['open', 'ssp-keyboard', 'just-work', 'pincode']
            for i in range(0, modes.length, 1):
                if modes[i] == mode:
                    val = i
                    break
        if val == -1:
            return
        self.send_command(*['SA,' + str(val)])

    def config_power(self, dbm):
        val = '0010'
        if 16 > dbm and dbm >= 12:
            val = '000C'
        elif 12 > dbm and dbm >= 8:
            val = '0008'
        elif 8 > dbm and dbm >= 4:
            val = '0004'
        elif 4 > dbm and dbm >= 0:
            val = '0000'
        elif 0 > dbm and dbm >= -4:
            val = 'FFFC'
        elif -4 > dbm and dbm >= -8:
            val = 'FFF8'
        elif -8 > dbm:
            val = 'FFF4'
        self.send_command(*['SY,' + str(val)])

    def config_get_setting(self):
        self.send_command(*['D'])

    def config_get_extend_setting(self):
        self.send_command(*['E'])