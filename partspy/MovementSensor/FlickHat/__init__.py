from attrdict import AttrDefault

import datetime

import asyncio

class FlickHat:
    def __init__(self):
        self.keys = ['vcc', 'gnd', 'sda', 'scl', 'reset', 'ts', 'led1', 'led2']
        self.required_keys = ['gnd', 'sda', 'scl', 'reset', 'ts']
        self.display_io_names = AttrDefault(bool, {'sda': 'sda', 'scl': 'scl', 'gnd': 'gnd', 'reset': 'reset', 'ts': 'ts'})

    @staticmethod
    def info():
        return AttrDefault(bool, {'name': 'FlickHat'})

    def wired(self, obniz):
        self.obniz = obniz
        self.address = 0x42
        if self.obniz.is_valid_io(*[self.params.vcc]):
            self.obniz.get_io(*[self.params.vcc]).drive(*['5v'])
            self.obniz.get_io(*[self.params.vcc]).output(*[True])
        self.obniz.get_io(*[self.params.gnd]).output(*[False])
        self.io_reset = self.obniz.get_io(*[self.params.reset])
        self.io_reset.drive(*['3v'])
        self.io_ts = self.obniz.get_io(*[self.params.ts])
        self.io_ts.drive(*['open-drain'])
        self.io_ts.pull(*['3v'])
        self.params.mode = 'master'
        self.params.pull = '3v'
        self.params.clock = 100 * 1000
        self.i2c = self.obniz.get_i2_cwith_config(*[self.params])
        if self.obniz.is_valid_io(*[self.params.led1]):
            self.led1 = self.obniz.wired(*['LED', AttrDefault(bool, {'anode': self.params.led1})])
        if self.obniz.is_valid_io(*[self.params.led2]):
            self.led2 = self.obniz.wired(*['LED', AttrDefault(bool, {'anode': self.params.led2})])

    async def start(self, callback_fw_info):
        self.io_ts.pull(*['3v'])
        self.io_reset.output(*[False])
        await self.obniz.wait(*[50])
        self.io_reset.output(*[True])
        await self.obniz.wait(*[50])
        self.onfwinfo = callback_fw_info
        self.fw_info = AttrDefault(bool, {'fw_valid': 0, 'fw_info_received': False})
        self.rotation = 0
        self.last_rotation = 0
        self.read_size = 132
        await self.polling()
        await self.obniz.wait(*[200])
        self.i2c.write(*[self.address, [0x10, 0x00, 0x00, 0xa2, 0xa1, 0x00, 0x00, 0x00, 0x1f, 0x00, 0x00, 0x00, 0xff, 0xff, 0xff, 0xff]])
        await self.obniz.wait(*[100])
        self.i2c.write(*[self.address, [0x10, 0x00, 0x00, 0xa2, 0x80, 0x00, 0x00, 0x00, 0x3f, 0x00, 0x00, 0x00, 0x3f, 0x00, 0x00, 0x00]])

    def _data_array2string(self, data):
        result = ''
        for n in data:
            result += _string.from_char_code(*[n])
        return result

    async def polling(self, timeout):
        timeout = timeout or 3000
        maskGestureInfo = 1 << 1
        maskTouchInfo = 1 << 2
        maskAirWheelInfo = 1 << 3
        maskXYZPosition = 1 << 4
        sysPositionValid = 1
        sysAirWheelValid = 1 << 1
        startTime = datetime.datetime.now()
        ts = True
        while ts and (datetime.datetime.now() - start_time) < timeout:
            ts = await self.io_ts.input_wait()
        if not ts:
            self.io_ts.pull(*['0v'])
            data = await self.i2c.read_wait(*[self.address, self.read_size])
            size = data[0]
            seq = data[2]
            msgID = data[3]
            if size != 0xff and size > 0:
                if self.debugprint or self.obniz.debugprint:
                    console.log(*['flickHat: ' + str(data.slice(*[0, size]).map(*[# TODO: ArrowFunctionExpression was here]))])
                configmask = None
                sysinfo = None
                gesture = None
                touch = None
                airwheel = None
                statusInfo = None
                fwInfo = None
                if msg_id==0x91:
                    configmask = data[4] or data[5] << 8
                    sysinfo = data[7]
                    gesture = data.slice(*[10, 14])
                    touch = data.slice(*[14, 18])
                    airwheel = data.slice(*[18, 20])
                    if gesture[0] == 255 and gesture[1] == 255 and gesture[2] == 255 and gesture[3] == 255:
                        break
                    if configmask and mask_xyzposition and sysinfo and sys_position_valid:
                        xyz = AttrDefault(bool, {'x': data[20] or data[21] << 8 / 65536, 'y': data[22] or data[23] << 8 / 65536, 'z': data[24] or data[25] << 8 / 65536, 'seq': seq})
                        self.xyz = xyz
                        if type(self.onxyz) == 'function':
                            self.onxyz(*[xyz])
                    if configmask and mask_gesture_info and gesture[0] > 0:
                        self.last_gesture = gesture[0]
                        gestures = [['', '', ''], ['garbage', '', ''], ['flick', 'west', 'east'], ['flick', 'east', 'west'], ['flick', 'south', 'north'], ['flick', 'north', 'south'], ['circle', 'clockwise', ''], ['circle', 'counter-clockwise', ''][], ['wave', 'y', ''], ['hold', '', '']]
                        for index, _ in enumerate(gestures):
                            if index == gesture[0] and type(self.ongestureall) == 'function':
                                self.ongestureall(*[AttrDefault(bool, {'action': gestures[index][0], 'from': gestures[index][1], 'to': gestures[index][2], 'raw': gesture, 'seq': seq})])
                            if index == gesture[0] and gestures[index][0] == 'flick' and type(self.ongesture) == 'function':
                                self.ongesture(*[AttrDefault(bool, {'action': 'gesture', 'from': gestures[index][1], 'to': gestures[index][2], 'raw': gesture, 'seq': seq})])
                    if configmask and mask_touch_info and not touch[0] == 0 and touch[1] == 0 and touch[3] == 0:
                        touchAction = touch[0] or touch[1] << 8
                        if touch_action == 0xffff:
                            break
                        actions = [['touch', 'south'], ['touch', 'west'], ['touch', 'north'], ['touch', 'east'], ['touch', 'center'], ['tap', 'south'], ['tap', 'west'], ['tap', 'north'], ['tap', 'east'], ['tap', 'center'], ['doubletap', 'south'], ['doubletap', 'west'], ['doubletap', 'north'], ['doubletap', 'east'], ['doubletap', 'center']]
                        touches = []
                        taps = []
                        doubletaps = []
                        self.last_touch = touch_action
                        comp = 1
                        for index, _ in enumerate(actions):
                            value = actions[index]
                            if touch_action and comp:
                                if value[0]=='touch':
                                    touches.push(*[value[1]])
                                elif value[0]=='tap':
                                    taps.push(*[value[1]])
                                elif value[0]=='doubletap':
                                    doubletaps.push(*[value[1]])
                                else:

                            comp <<= 1
                        if touches.length > 0 and type(self.ontouch) == 'function':
                            self.ontouch(*[AttrDefault(bool, {'action': 'touch', 'positions': touches, 'raw': touch, 'seq': seq})])
                        if taps.length > 0 and type(self.ontap) == 'function':
                            self.ontap(*[AttrDefault(bool, {'action': 'tap', 'positions': taps, 'raw': touch, 'seq': seq})])
                        if doubletaps.length > 0 and type(self.ondoubletap) == 'function':
                            self.ondoubletap(*[AttrDefault(bool, {'action': 'doubletap', 'positions': doubletaps, 'raw': touch, 'seq': seq})])
                    if configmask and mask_air_wheel_info and sysinfo and sys_air_wheel_valid:
                        delta = (airwheel[0] - self.last_rotation) / 32.0
                        self.rotation += delta * 360.0
                        self.rotation %= 360
                        if delta != 0 and delta > -0.5 and delta < 0.5:
                            if type(self.onairwheel) == 'function':
                                self.onairwheel(*[AttrDefault(bool, {'delta': delta * 360.0, 'rotation': self.rotation, 'raw': airwheel, 'seq': seq})])
                        self.last_rotation = airwheel[0]
                elif msg_id==0x15:
                    status_info = AttrDefault(bool, {'msg_id': data[4], 'max_cmd_size': data[5], 'error': data[6] or data[7] << 8})
                    self.status_info = status_info
                    if self.debugprint or self.obniz.debugprint:
                        console.log(*["flickHat: system status: {msgId: " + status_info.msg_id + ", maxCmdSize: " + status_info.max_cmd_size + ", error: " + status_info.error + "}"])
                elif msg_id==0x83:
                    fw_info = AttrDefault(bool, {'fw_valid': data[4] == 0xaa, 'hw_rev': [data[5], data[6]], 'param_start_addr': data[7] * 128, 'lib_loader_ver': [data[8], data[9]], 'lib_loader_platform': data[10], 'fw_start_addr': data[11] * 128, 'fw_version': self._data_array2string(*[data.slice(*[12, 132])]).split(*['\0'])[0], 'fw_info_received': True})
                    self.fw_info = fw_info
                    if type(self.onfwinfo) == 'function':
                        self.onfwinfo(*[fw_info])
                    self.read_size = 26
                else:
                    console.error(*["unknown message: 0x" + msg_id.to_string(*[16]) + ", data:" + data.slice(*[0, size]).map(*[# TODO: ArrowFunctionExpression was here]) + ""])
            self.io_ts.pull(*['3v'])