class _7_segment_led:
    def __init__(self):
        self.keys = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'dp', 'common', 'commonType']
        self.required_keys = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
        self.digits = [0x3f, 0x06, 0x5b, 0x4f, 0x66, 0x6d, 0x7d, 0x07, 0x7f, 0x6f, 0x6f]
        self.display_io_names = {'a': 'a', 'b': 'b', 'c': 'c', 'd': 'd', 'e': 'e', 'f': 'f', 'g': 'g', 'dp': 'dp', 'common': 'com'}

    @staticmethod
    def info():
        return {'name': '7SegmentLED'}

    def wired(self, obniz):
        def get_io(io):
            if io and type(io) == 'object':
                if type(io['output']) == 'function':
                    return io
            return obniz.get_io(*[io])

        def is_valid_io(io):
            if io and type(io) == 'object':
                if type(io['output']) == 'function':
                    return True
            return obniz.is_valid_io(*[io])

        self.obniz = obniz
        self.ios = []
        self.ios.push(*[get_io(*[self.params.a])])
        self.ios.push(*[get_io(*[self.params.b])])
        self.ios.push(*[get_io(*[self.params.c])])
        self.ios.push(*[get_io(*[self.params.d])])
        self.ios.push(*[get_io(*[self.params.e])])
        self.ios.push(*[get_io(*[self.params.f])])
        self.ios.push(*[get_io(*[self.params.g])])
        self.is_cathode_common = False if self.params.common_type == 'anode' else True
        # TODO: failed to generate FOR statement
        if is_valid_io(*[self.params.dp]):
            self.dp = get_io(*[self.params.dp])
            self.dp.output(*[False])
        if is_valid_io(*[self.params.common]):
            self.common = get_io(*[self.params.common])
            self.on()

    def print(self, data):
        if type(data) == 'number':
            data = parse_int(*[data])
            data = data % 10
            # TODO: failed to generate FOR statement
            self.on()

    def print_raw(self, data):
        if type(data) == 'number':
            # TODO: failed to generate FOR statement
            self.on()

    def dp_state(self, show):
        if self.dp:
            self.dp.output(*[show if self.is_cathode_common else not show])

    def on(self):
        self.common.output(*[False if self.is_cathode_common else True])

    def off(self):
        self.common.output(*[True if self.is_cathode_common else False])