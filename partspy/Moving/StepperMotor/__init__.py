import asyncio

class _stepper_motor:
    def __init__(self):
        self.keys = ['a', 'b', 'aa', 'bb', 'common']
        self.required_keys = ['a', 'b', 'aa', 'bb']
        self._step_instructions = {'1': [[0, 1, 1, 1], [1, 0, 1, 1], [1, 1, 0, 1], [1, 1, 1, 0]],'2': [[0, 0, 1, 1], [1, 0, 0, 1], [1, 1, 0, 0], [0, 1, 1, 0]],'1-2': [[0, 1, 1, 1], [0, 0, 1, 1], [1, 0, 1, 1], [1, 0, 0, 1], [1, 1, 0, 1], [1, 1, 0, 0], [1, 1, 1, 0], [0, 1, 1, 0]}
        self.type = undefined
        self.current_step = 0
        self._step_type = '2'
        self.frequency = 100
        self.rotation_step_count = 100
        self.milli_meter_step_count = 1

    @staticmethod
    def info():
        return {'name': 'StepperMotor'}

    def wired(self, obniz):
        self.obniz = obniz
        if obniz.is_valid_io(*[self.params.common]):
            self.common = obniz.get_io(*[self.params.common])
            self.common.output(*[True])
            self.type = 'unipolar'
        else:
            self.type = 'bipolar'
        self.ios = []
        self.ios.push(*[obniz.get_io(*[self.params.a])])
        self.ios.push(*[obniz.get_io(*[self.params.b])])
        self.ios.push(*[obniz.get_io(*[self.params.aa])])
        self.ios.push(*[obniz.get_io(*[self.params.bb])])

    async def step_wait(self, step_count):
        if step_count == 0:
            return
        step_count_abs = _math.abs(*[step_count])
        instructions = self._get_step_instructions()
        instruction_length = instructions.length
        array = []
        currentPhase = self.current_step % instruction_length
        if current_phase < 0:
            current_phase = instruction_length - current_phase * -1
        if step_count > 0:
            for i in range(0, instructions.length, 1):
                if  >= instruction_length:
                    current_phase = 0
                array.push(*[instructions[currentPhase]])
        else:
            for i in range(0, instructions.length, 1):
                if  < 0:
                    current_phase = instruction_length - 1
                array.push(*[instructions[currentPhase]])
        msec = 1000 / self.frequency
        msec = parse_int(*[msec])
        if msec < 1:
            msec = 1
        state = # TODO: ArrowFunctionExpression was here
        states = []
        for i in range(0, instruction_length, 1):
            states.push(*[{'duration': msec, 'state': state}])
        await self.obniz.io.repeat_wait(*[states, step_count_abs])
        self.current_step += step_count

    async def step_to_wait(self, destination):
        mustmove = destination - self.current_step
        await self.step_wait(*[mustmove])

    async def hold_wait(self):
        instructions = self._get_step_instructions()
        instruction_length = instructions.length
        currentPhase = self.current_step % instruction_length
        if current_phase < 0:
            current_phase = instruction_length - current_phase * -1
        for i in range(0, self.ios.length, 1):
            self.ios[i].output(*[instructions[currentPhase][i]])
        await self.obniz.ping_wait()

    async def free_wait(self):
        for i in range(0, self.ios.length, 1):
            self.ios[i].output(*[True])
        await self.obniz.ping_wait()

    def step_type(self, step_type):
        newType = self._step_instructions[stepType]
        if not new_type:
            raise Exception('unknown step type ' + str(step_type))
        self._step_type = step_type

    def speed(self, step_per_sec):
        self.frequency = step_per_sec

    def current_rotation(self):
        return self.current_step / self.rotation_step_count * 360

    def current_angle(self):
        angle = parse_int(*[self.current_rotation() * 1000]) % 360000 / 1000
        if angle < 0:
            angle = 360 - angle
        return angle

    async def rotate_wait(self, rotation):
        rotation /= 360
        needed = rotation * self.rotation_step_count
        await self.step_wait(*[needed])

    async def rotate_to_wait(self, angle):
        needed = angle - self.current_angle()
        if _math.abs(*[needed]) > 180:
            needed = needed - 360 if needed > 0 else 360 + needed
        needed = needed / 360 * self.rotation_step_count
        await self.step_wait(*[needed])

    def current_distance(self):
        return self.current_step / self.milli_meter_step_count

    async def move_wait(self, distance):
        needed = distance * self.milli_meter_step_count
        await self.step_wait(*[needed])

    async def move_to_wait(self, destination):
        needed = destination - self.current_distance() * self.milli_meter_step_count
        await self.step_wait(*[needed])

    def _get_step_instructions(self):
        return self._step_instructions[self._step_type]