from attrdict import AttrDefault

import asyncio

class XBee:
    def __init__(self):
        self.keys = ['tx', 'rx', 'gnd']
        self.required_keys = ['tx', 'rx']
        self.display_io_names = AttrDefault(bool, {'tx': '<tx', 'rx': '>rx'})

    @staticmethod
    def info():
        return AttrDefault(bool, {'name': 'XBee'})

    def wired(self, obniz):
        self.uart = obniz.get_free_uart()
        self.current_command = null
        self.commands = []
        self.is_at_mode = False
        self.on_finish_at_mode_callback = null
        if type(self.params.gnd) == 'number':
            obniz.get_io(*[self.params.gnd]).output(*[False])
        self.uart.start(*[AttrDefault(bool, {'tx': self.params.tx, 'rx': self.params.rx, 'baud': 9600, 'drive': '3v'})])
        self.uart.onreceive = # TODO: failed to generate Function Expression

    def send(self, text):
        if self.is_at_mode == False:
            self.uart.send(*[text])
        else:
            self.obniz.error(*['XBee is AT Command mode now. Wait for finish config.'])

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
            self.obniz.error(*['XBee config error : ' + str(self.current_command)])
        else:
            console.log(*['XBEE : no catch message', data])
            next()

    def add_command(self, command, value):
        str = (command + ' ' + str(value) if value else '')
        self.commands.push(*[str])
        if self.is_at_mode == True and self.current_command == null:
            self.send_command()

    def send_command(self):
        if self.is_at_mode == True and self.current_command == null and self.commands.length > 0:
            self.current_command = 'AT' + str(self.commands.shift())
            self.uart.send(*[str(self.current_command) + '\r'])

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