class _sharp_memory_tft:
    def __init__(self):
        self.keys = ['vcc', 'gnd', 'vcc_a', 'gnd_a', 'sclk', 'mosi', 'cs', 'disp', 'extcomin', 'extmode', 'width', 'height']
        self.required_keys = ['sclk', 'mosi', 'cs', 'width', 'height']
        self.commands = }
        self.commands.write = 0x80
        self.commands.clear = 0x20
        self.commands.vcom = 0x40
        self._canvas = null
        self._reset()

    @staticmethod
    def info():
        return {'name': 'SharpMemoryTFT'}

    def wired(self, obniz):
        self.obniz = obniz
        self.io_cs = obniz.get_io(*[self.params.cs])
        if self.params.disp and self.params.extcomin and self.params.extmode:
            self.io_disp = obniz.get_io(*[self.params.disp])
            self.io_extcomin = obniz.get_io(*[self.params.extcomin])
            self.io_extmode = obniz.get_io(*[self.params.extmode])
            self.io_disp.output(*[True])
            self.io_extcomin.output(*[False])
            self.io_extmode.output(*[False])
        obniz.set_vcc_gnd(*[self.params.vcc, self.params.gnd, '5v'])
        obniz.set_vcc_gnd(*[self.params.vcc_a, self.params.gnd_a, '5v'])
        self.params.mode = 'master'
        self.params.frequency = parse_int(*[1000 * 1000])
        self.params.clk = self.params.sclk
        self.params.drive = '5v'
        self.spi = self.obniz.get_spi_with_config(*[self.params])
        self.width = self.params.width
        self.height = self.params.height
        self.obniz.wait(*[100])

    def _reverse_bits(self, data):
        revData = 0
        # TODO: failed to generate FOR statement
        return rev_data

    def send_lsb(self, data):
        self.spi.write(*[[self._reverse_bits(*[data])]])

    def send_clear(self):
        self.io_cs.output(*[True])
        self.spi.write(*[[self.commands.clear or 0x00, 0x00]])
        self.io_cs.output(*[False])

    def raw(self, raw_data):
        oldline = None
        currentline = None
        totalbytes = self.width * self.height / 8
        array = [0] * 1024
        index = 0
        array[] = self.commands.write or self.commands.vcom
        oldline = currentline = 1
        array[] = self._reverse_bits(*[currentline])
        self.io_cs.output(*[True])
        # TODO: failed to generate FOR statement
        if index > 0:
            self.spi.write(*[array.slice(*[0, index])])
        self.spi.write(*[[0x00]])
        self.io_cs.output(*[False])

    def _reset(self):
        self._pos = {'x': 0, 'y': 0}
        self.auto_flush = True

    def warn_canvas_availability(self):
        if self.obniz.is_node:
            raise Exception('MemoryDisplay require node-canvas to draw rich contents. see more detail on docs')
        else:
            raise Exception('MemoryDisplay require node-canvas to draw rich contents. see more detail on docs')

    def _prepared_canvas(self):
        if self._canvas:
            return self._canvas
        if self.obniz.is_node:
            # TODO: failed to TRY statement
        else:
            # TODO: failed to TRY statement
        ctx = self._canvas.get_context(*['2d'])
        ctx.fill_style = '#FFF'
        ctx.fill_rect(*[0, 0, self.width, self.height])
        ctx.fill_style = '#000'
        ctx.stroke_style = '#000'
        self._pos.x = 0
        self._pos.y = 0
        self.font_size = 16
        ctx.font = self.font_sizepx Arial
        return self._canvas

    def _ctx(self):
        canvas = self._prepared_canvas()
        if canvas:
            return canvas.get_context(*['2d'])

    def font(self, font, size):
        ctx = self._ctx()
        if type(size) != 'number':
            size = 16
        if type(font) != 'string':
            font = 'Arial'
        self.font_size = size
        ctx.font = '' + +' ' + size + 'px ' + font

    def clear(self):
        ctx = self._ctx()
        self._pos.x = 0
        self._pos.y = 0
        if ctx:
            ctx.fill_style = '#fff'
            ctx.fill_rect(*[0, 0, self.width, self.height])
            ctx.fill_style = '#000'
            ctx.stroke_style = '#000'
            self.draw(*[ctx])
        else:
            ctx.fill_style = '#fff'
            ctx.fill_rect(*[0, 0, self.width, self.height])
            ctx.fill_style = '#000'
            ctx.stroke_style = '#000'
            self.draw(*[ctx])

    def pos(self, x, y):
        self._ctx()
        if type(x) == 'number':
            self._pos.x = x
        if type(y) == 'number':
            self._pos.y = y
        return self._pos

    def print(self, text):
        ctx = self._ctx()
        if ctx:
            ctx.fill_text(*[text, self._pos.x, self._pos.y + self.font_size])
            self.draw(*[ctx])
            self._pos.y += self.font_size
        else:
            ctx.fill_text(*[text, self._pos.x, self._pos.y + self.font_size])
            self.draw(*[ctx])
            self._pos.y += self.font_size

    def line(self, x_0, y_0, x_1, y_1):
        ctx = self._ctx()
        if ctx:
            ctx.begin_path()
            ctx.move_to(*[x_0, y_0])
            ctx.line_to(*[x_1, y_1])
            ctx.stroke()
            self.draw(*[ctx])
        else:
            ctx.begin_path()
            ctx.move_to(*[x_0, y_0])
            ctx.line_to(*[x_1, y_1])
            ctx.stroke()
            self.draw(*[ctx])

    def rect(self, x, y, width, height, must_fill):
        ctx = self._ctx()
        if ctx:
            if must_fill:
                ctx.fill_rect(*[x, y, width, height])
            else:
                ctx.fill_rect(*[x, y, width, height])
            self.draw(*[ctx])
        else:
            if must_fill:
                ctx.fill_rect(*[x, y, width, height])
            else:
                ctx.fill_rect(*[x, y, width, height])
            self.draw(*[ctx])

    def circle(self, x, y, r, must_fill):
        ctx = self._ctx()
        if ctx:
            ctx.begin_path()
            ctx.arc(*[x, y, r, 0, _math._pi * 2])
            if must_fill:
                ctx.fill()
            else:
                ctx.fill()
            self.draw(*[ctx])
        else:
            ctx.begin_path()
            ctx.arc(*[x, y, r, 0, _math._pi * 2])
            if must_fill:
                ctx.fill()
            else:
                ctx.fill()
            self.draw(*[ctx])

    def _draw(self, ctx):
        stride = self.width / 8
        vram = [0] * stride * 64
        imageData = ctx.get_image_data(*[0, 0, self.width, self.height])
        data = image_data.data
        # TODO: failed to generate FOR statement
        self.raw(*[vram])

    def draw(self, ctx):
        if self.auto_flush:
            self._draw(*[ctx])

    def drawing(self, auto_flush):
        self.auto_flush = auto_flush == True
        ctx = self._ctx()
        if ctx:
            self.draw(*[ctx])