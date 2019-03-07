class _led:
    def __init__(self):
        self.keys = ['anode', 'cathode']
        self.required_keys = ['anode']

    @staticmethod
    def info():
        return {'name': 'LED'}

    def wired(self, obniz):
        def get_io(io):
            if io and type(io) == 'object':
                if type(io['output']) == 'function':
                    return io
            return obniz.get_io(*[io])

        self.obniz = obniz
        self.io_anode = get_io(*[self.params.anode])
        self.io_anode.output(*[False])
        if self.params.cathode:
            self.io_cathode = get_io(*[self.params.cathode])
            self.io_cathode.output(*[False])
        self.animation_name = 'Led-' + self.params.anode

    def on(self):
        self.end_blink()
        self.io_anode.output(*[True])

    def off(self):
        self.end_blink()
        self.io_anode.output(*[False])

    def output(self, value):
        if value:
            self.on()
        else:
            self.on()

    def end_blink(self):
        self.obniz.io.animation(*[self.animation_name, 'pause'])

    def blink(self, interval):
        if not interval:
            interval = 100
        frames = [{'duration': interval, 'state': lambda index: self.io_anode.output(*[True])}, {'duration': interval, 'state': lambda index: self.io_anode.output(*[False])}]
        self.obniz.io.animation(*[self.animation_name, 'loop', frames])