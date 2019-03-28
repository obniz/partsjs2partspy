from attrdict import AttrDefault

class SharpMemoryTFT:
    def __init__(self):
        self.keys = ['vcc', 'gnd', 'vcc_a', 'gnd_a', 'sclk', 'mosi', 'cs', 'disp', 'extcomin', 'extmode', 'width', 'height']
        self.required_keys = ['sclk', 'mosi', 'cs', 'width', 'height']
        self.commands = AttrDict({})
        self.commands.write = 0x80
        self.commands.clear = 0x20
        self.commands.vcom = 0x40
        self._canvas = null
        self._reset()

    @staticmethod
    def info():
        return AttrDefault(bool, {'name': 'SharpMemoryTFT'})

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
        for i in range(0, 8, 1):
            rev_data += data and 0x01
            data >>= 1
            if i < 7:
                rev_data <<= 1
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
        for i in range(0, totalbytes, 1):
            array[] = raw_data[i]
            currentline = parse_int(*[((i + 1) / self.width / 8 + 1), 10])
            if currentline != oldline:
                array[] = 0x00
                if currentline <= self.height:
                    array[] = self._reverse_bits(*[currentline])
                oldline = currentline
            if index >= 1021:
                self.spi.write(*[array.slice(*[0, index])])
                array = [0] * 1024
                index = 0
        if index > 0:
            self.spi.write(*[array.slice(*[0, index])])
        self.spi.write(*[[0x00]])
        self.io_cs.output(*[False])

    def _reset(self):
        self._pos = AttrDefault(bool, {'x': 0, 'y': 0})
        self.auto_flush = True

    def warn_canvas_availability(self):
        if self.obniz.is_node:
            raise Exception('MemoryDisplay require node-canvas to draw rich contents. see more detail on docs')
        else:
            raise Exception('MemoryDisplay cant create canvas element to body')

    def _prepared_canvas(self):
        if self._canvas:
            return self._canvas
        if self.obniz.is_node:
            # TODO: failed to TRY statement
        else:
            identifier = 'MemoryDispCanvas-' + str(self.obniz.id)
            canvas = document.get_element_by_id(*[identifier])
            if not canvas:
                canvas = document.create_element(*['canvas'])
                canvas.set_attribute(*['id', identifier])
                canvas.style.visibility = 'hidden'
                canvas.width = self.width
                canvas.height = self.height
                canvas.style['-webkit-font-smoothing'] = 'none'
                body = document.get_elements_by_tag_name(*['body'])[0]
                body.append_child(*[canvas])
            self._canvas = canvas
        ctx = self._canvas.get_context(*['2d'])
        ctx.fill_style = '#FFF'
        ctx.fill_rect(*[0, 0, self.width, self.height])
        ctx.fill_style = '#000'
        ctx.stroke_style = '#000'
        self._pos.x = 0
        self._pos.y = 0
        self.font_size = 16
        ctx.font = "" + self.font_size + "px Arial"
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
        ctx.font = (str(('' + str(+' ') + size)) + 'px ' + font)

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
            self.send_clear()

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
            ctx.fill_text(*[text, self._pos.x, (self._pos.y + self.font_size)])
            self.draw(*[ctx])
            self._pos.y += self.font_size
        else:


    def line(self, x_0, y_0, x_1, y_1):
        ctx = self._ctx()
        if ctx:
            ctx.begin_path()
            ctx.move_to(*[x_0, y_0])
            ctx.line_to(*[x_1, y_1])
            ctx.stroke()
            self.draw(*[ctx])
        else:
            self.warn_canvas_availability()

    def rect(self, x, y, width, height, must_fill):
        ctx = self._ctx()
        if ctx:
            if must_fill:
                ctx.fill_rect(*[x, y, width, height])
            else:
                ctx.stroke_rect(*[x, y, width, height])
            self.draw(*[ctx])
        else:
            self.warn_canvas_availability()

    def circle(self, x, y, r, must_fill):
        ctx = self._ctx()
        if ctx:
            ctx.begin_path()
            ctx.arc(*[x, y, r, 0, _math.PI * 2])
            if must_fill:
                ctx.fill()
            else:
                ctx.stroke()
            self.draw(*[ctx])
        else:
            self.warn_canvas_availability()

    def _draw(self, ctx):
        stride = self.width / 8
        vram = [0] * stride * 64
        imageData = ctx.get_image_data(*[0, 0, self.width, self.height])
        data = image_data.data
        for i in range(0, data.length, 4):
            brightness = ((0.34 * data[i] + 0.5 * data[(i + 1)]) + 0.16 * data[(i + 2)])
            index = parse_int(*[i / 4])
            line = parse_int(*[index / self.width])
            col = parse_int(*[(index - line * self.width) / 8])
            bits = parse_int(*[(index - line * self.width)]) % 8
            if bits == 0:
                vram[(line * stride + col)] = 0x00
            if brightness > 0x73:
                vram[(line * stride + col)] |= 0x80 >> bits
        self.raw(*[vram])

    def draw(self, ctx):
        if self.auto_flush:
            self._draw(*[ctx])

    def drawing(self, auto_flush):
        self.auto_flush = auto_flush == True
        ctx = self._ctx()
        if ctx:
            self.draw(*[ctx])