import asyncio

class OMRON_2JCIE:
    def __init__(self):
        self.keys = []
        self.required_keys = []
        self.periperal = null

    @staticmethod
    def info():
        return {'name': '2JCIE'}

    def wired(self, obniz):
        self.obniz = obniz

    async def find_wait(self):
        target = {'local_name': 'Envd'}
        self.periperal = await self.obniz.ble.scan.start_one_wait(*[target])
        return self.periperal

    def omron_uuid(self, uuid):
        return "0C4C" + uuid + "-7700-46F4-AA96D5E974E32A54"

    async def connect_wait(self):
        if not self.periperal:
            await self.find_wait()
        if not self.periperal:
            raise Exception('2JCIE not found')
        if not self.periperal.connected:
            await self.periperal.connect_wait()

    async def disconnect_wait(self):
        if self.periperal and self.periperal.connected:
            self.periperal.disconnect_wait()

    def signed_number_from_binary(self, data):
        val = data[data.length - 1] and 0x7f
        for i in range(data.length - 2, 0 - 1, -1):
            val = val * 256 + data[i]
        if data[data.length - 1] and 0x80 != 0:
            val = val - _math.pow(*[2, data.length * 8 - 1])
        return val

    def unsigned_number_from_binary(self, data):
        val = data[data.length - 1]
        for i in range(data.length - 2, 0 - 1, -1):
            val = val * 256 + data[i]
        return val

    async def get_latest_data(self):
        await self.connect_wait()
        c = self.periperal.get_service(*[self.omron_uuid(*['3000'])]).get_characteristic(*[self.omron_uuid(*['3001'])])
        data = await c.read_wait()
        json = {'row_number': data[0], 'temperature': self.signed_number_from_binary(*[data.slice(*[1, 3])]) * 0.01, 'relative_humidity': self.signed_number_from_binary(*[data.slice(*[3, 5])]) * 0.01, 'light': self.signed_number_from_binary(*[data.slice(*[5, 7])]) * 1, 'uv_index': self.signed_number_from_binary(*[data.slice(*[7, 9])]) * 0.01, 'barometric_pressure': self.signed_number_from_binary(*[data.slice(*[9, 11])]) * 0.1, 'soud_noise': self.signed_number_from_binary(*[data.slice(*[11, 13])]) * 0.01, 'discomfort_index': self.signed_number_from_binary(*[data.slice(*[13, 15])]) * 0.01, 'heatstroke_risk_factor': self.signed_number_from_binary(*[data.slice(*[15, 17])]) * 0.01, 'battery_voltage': self.unsigned_number_from_binary(*[data.slice(*[17, 19])]) * 0.001}
        return json