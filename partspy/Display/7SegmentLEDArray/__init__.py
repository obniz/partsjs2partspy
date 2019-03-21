import datetime

class _7_segment_ledarray:
    def __init__(self):
        self.identifier = '' + str(datetime.datetime.now().get_time())
        self.keys = ['segments']
        self.required_keys = self.keys

    @staticmethod
    def info():
        return {'name': '7SegmentLEDArray'}

    def wired(self, obniz):
        self.obniz = obniz
        self.segments = self.params.segments

    def print(self, data):
        if type(data) == 'number':
            data = parse_int(*[data])
            print = # TODO: ArrowFunctionExpression was here
            animations = []
            for i in range(0, self.segments.length, 1):
                animations.push(*[{'duration': 3, 'state': print}])
            self.obniz.io.animation(*[self.identifier, 'loop', animations])

    def on(self):
        self.obniz.io.animation(*[self.identifier, 'resume'])

    def off(self):
        self.obniz.io.animation(*[self.identifier, 'pause'])
        for i in range(0, self.segments.length, 1):
            self.segments[i].off()