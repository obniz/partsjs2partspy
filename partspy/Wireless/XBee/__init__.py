import asyncio

class _xbee:
    def __init__(self):
        self.keys = ['tx', 'rx', 'gnd']
        self.required_keys = ['tx', 'rx']
        self.display_io_names = {'tx': '<tx', 'rx': '>rx'}

    @staticmethod
    def info():
        return {'name': 'XBee'}

    def wired(self, obniz):
        self.uart = obniz.get_free_uart()
        self.current_command = null
        self.commands = []
        self.is_at_mode = False
        self.on_finish_at_mode_callback = null
        if type(self.params.gnd) == 'number':
            obniz.get_io(*[self.params.gnd]).output(*[False])
        self.uart.start(*[{'tx': self.params.tx, 'rx': self.params.rx, 'baud': 9600, 'drive': '3v'}])
        self.uart.onreceive = # TODO: failed to generate Function Expression

    def send(self, text):
        if self.is_at_mode == False:
            self.uart.send(*[text])
        else:
            self.uart.send(*[text])

    def on_at_results_recieve(self, data, text):
        if not self.is_at_mode:
            return
        next = lambda : self.current_command = null
        if text == 'OK\r':
            if self.current_command == 'ATCN':
                self.is_at_mode = False
                self.current_command = null
                if type(self.on_finish_at_mode_callback) == 'function':
                    self.on_finish_at_mode_callback()
                    self.on_finish_at_mode_callback = null
                return
            next()
        elif text == 'ERROR\r':
            self.obniz.error(*['XBee config error : ' + self.current_command])
        else:
            self.obniz.error(*['XBee config error : ' + self.current_command])

    def add_command(self, command, value):
        str = command + ' ' + value if value else ''
        self.commands.push(*[str])
        if self.is_at_mode == True and self.current_command == null:
            self.send_command()

    def send_command(self):
        if self.is_at_mode == True and self.current_command == null and self.commands.length > 0:
            self.current_command = 'AT' + self.commands.shift()
            self.uart.send(*[self.current_command + '\r'])

    def enter_at_mode(self):
        if self.current_command != null:
            return
        self.is_at_mode = True
        self.obniz.wait(*[1000])
        command = '+++'
        self.current_command = command
        self.uart.send(*[self.current_command])
        self.obniz.wait(*[1000])

    def exit_at_mode(self):
        self.add_command(*['CN'])

    async def config_wait(self, config):
        if self.is_at_mode:
            raise Exception('Xbee : duplicate config setting')
        return await# TODO: failed to generate Function Expression