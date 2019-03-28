from attrdict import AttrDefault

import datetime

import asyncio

class SainSmartTFT18LCD:
    def __init__(self):
        self.keys = ['vcc', 'gnd', 'scl', 'sda', 'dc', 'res', 'cs']
        self.required = ['scl', 'sda', 'dc', 'res', 'cs']
        self.display_io_names = AttrDefault(bool, {'vcc': 'vcc', 'gnd': 'gnd', 'scl': 'scl', 'sda': 'sda', 'dc': 'dc', 'res': 'res', 'cs': 'cs'})

    @staticmethod
    def info():
        return AttrDefault(bool, {'name': 'SainSmartTFT18LCD'})

    def wired(self, obniz):
        self.debugprint = False
        self.obniz = obniz
        self.io_dc = obniz.get_io(*[self.params.dc])
        self.io_res = obniz.get_io(*[self.params.res])
        self.io_cs = obniz.get_io(*[self.params.cs])
        self.obniz.set_vcc_gnd(*[self.params.vcc, self.params.gnd, '5v'])
        self.params.frequency = 16 * 1000 * 1000
        self.params.mode = 'master'
        self.params.clk = self.params.scl
        self.params.mosi = self.params.sda
        self.params.drive = '3v'
        self.spi = self.obniz.get_spi_with_config(*[self.params])
        self.io_dc.output(*[True])
        self.io_cs.output(*[False])
        self.width = ST7735_TFTWIDTH
        self.height = ST7735_TFTHEIGHT
        self.write_buffer = []
        self._set_preset_color()
        self.init()

    def print_debug(self, v):
        if self.debugprint:
            console.log(*['SainSmartTFT18LCD: ' + str(_array.prototype.slice.call(*[arguments]).join(*['']))])

    def _dead_sleep(self, wait_msec):
        startMsec = datetime.datetime.now()
        while (datetime.datetime.now() - start_msec) < wait_msec:


    def _reset(self):
        self.io_res.output(*[False])
        self._dead_sleep(*[10])
        self.io_res.output(*[True])
        self._dead_sleep(*[10])

    def write_command(self, cmd):
        self.io_dc.output(*[False])
        self.io_cs.output(*[False])
        self.spi.write(*[[cmd]])
        self.io_cs.output(*[True])

    def write_data(self, data):
        self.io_dc.output(*[True])
        self.io_cs.output(*[False])
        self.spi.write(*[data])
        self.io_cs.output(*[True])

    def write(self, cmd, data):
        if data.length == 0:
            return
        self.write_command(*[cmd])
        self.write_data(*[data])

    async def asyncwait(self):
        return await self.spi.write_wait(*[[0x00]])

    def _write_flush(self):
        while self.write_buffer.length > 0:
            if self.write_buffer.length > 1024:
                data = self.write_buffer.slice(*[0, 1024])
                self.write_data(*[data])
                self.write_buffer.splice(*[0, 1024])
            else:
                if self.write_buffer.length > 0:
                    self.write_data(*[self.write_buffer])
                self.write_buffer = []

    def _write_buffer(self, data):
        if data and data.length > 0:
            self.write_buffer = self.write_buffer.concat(*[data])
        else:
            self._write_flush()

    def color16(self, r, g, b):
        return r and 0xf8 << 8 or g and 0xfc << 3 or b >> 3

    def _init_g(self):
        self.write_command(*[ST7735_SLPOUT])
        self.obniz.wait(*[120])
        self.write(*[ST7735_FRMCTR1, [0x01, 0x2c, 0x2d]])
        self.write(*[ST7735_FRMCTR2, [0x01, 0x2c, 0x2d]])
        self.write(*[ST7735_FRMCTR3, [0x01, 0x2c, 0x2d, 0x01, 0x2c, 0x2d]])
        self.write(*[ST7735_INVCTR, [0x07]])
        self.write(*[ST7735_PWCTR1, [0xa2, 0x02, 0x84]])
        self.write(*[ST7735_PWCTR2, [0xc5]])
        self.write(*[ST7735_PWCTR3, [0x0a, 0x00]])
        self.write(*[ST7735_PWCTR4, [0x8a, 0x2a]])
        self.write(*[ST7735_PWCTR5, [0x8a, 0xee]])
        self.write(*[ST7735_VMCTR1, [0x0e]])
        self.write(*[ST7735_GMCTRP1, [0x02, 0x1c, 0x07, 0x12, 0x37, 0x32, 0x29, 0x2d, 0x29, 0x25, 0x2b, 0x39, 0x00, 0x01, 0x03, 0x10]])
        self.write(*[ST7735_GMCTRN1, [0x03, 0x1d, 0x07, 0x06, 0x2e, 0x2c, 0x29, 0x2d, 0x2e, 0x2e, 0x37, 0x3f, 0x00, 0x00, 0x02, 0x10]])
        self.write(*[ST7735_COLMOD, [_st7735_16bit]])

    def init(self):
        self._reset()
        self._init_g()
        self.set_display_on()
        self.set_rotation(*[0])

    def set_display_on(self):
        self.write_command(*[ST7735_DISPON])

    def set_display_off(self):
        self.write_command(*[ST7735_DISPOFF])

    def set_display(self, on):
        if on == True:
            self.set_display_on()
        else:
            self.set_display_off()

    def set_inversion_on(self):
        self.write_command(*[ST7735_INVON])

    def set_inversion_off(self):
        self.write_command(*[ST7735_INVOFF])

    def set_inversion(self, inversion):
        if inversion == True:
            self.set_inversion_on()
        else:
            self.set_inversion_off()

    def set_rotation(self, m):
        MADCTL_MY = 0x80
        MADCTL_MX = 0x40
        MADCTL_MV = 0x20
        MADCTL_RGB = 0x00
        data = None
        rotation = m % 4
        if rotation==0:
            data = [MADCTL_MX or MADCTL_MY or MADCTL_RGB]
            self.width = ST7735_TFTWIDTH
            self.height = ST7735_TFTHEIGHT
        elif rotation==1:
            data = [MADCTL_MY or MADCTL_MV or MADCTL_RGB]
            self.width = ST7735_TFTHEIGHT
            self.height = ST7735_TFTWIDTH
        elif rotation==2:
            data = [MADCTL_RGB]
            self.width = ST7735_TFTWIDTH
            self.height = ST7735_TFTHEIGHT
        elif rotation==3:
            data = [MADCTL_MX or MADCTL_MV or MADCTL_RGB]
            self.width = ST7735_TFTHEIGHT
            self.height = ST7735_TFTWIDTH
        self.write(*[ST7735_MADCTL, data])
        self.set_addr_window(*[0, 0, (self.width - 1), (self.height - 1)])

    def set_addr_window(self, x0, y0, x1, y1):
        self.print_debug(*["setAddrWindow: (x0: " + x0 + ", y0: " + y0 + ") - (x1: " + x1 + ", y1: " + y1 + ")"])
        if x0 < 0:
            x0 = 0
        if y0 < 0:
            y0 = 0
        if x1 < 0:
            x1 = 0
        if y1 < 0:
            y1 = 0
        self.write(*[ST7735_CASET, [0x00, x0, 0x00, x1]])
        self.write(*[ST7735_RASET, [0x00, y0, 0x00, y1]])
        self.write_command(*[ST7735_RAMWR])
        self.write_buffer = []

    def fill_screen(self, color):
        self.fill_rect(*[0, 0, self.width, self.height, color])

    def fill_rect(self, x, y, w, h, color):
        if x >= self.width or y >= self.height:
            return
        if ((x + w) - 1) >= self.width:
            w = (self.width - x)
        if ((y + h) - 1) >= self.height:
            h = (self.height - y)
        self.set_addr_window(*[x, y, ((x + w) - 1), ((y + h) - 1)])
        hi = color >> 8
        lo = color and 0xff
        data = []
        # TODO: failed to generate FOR statement
        self._write_buffer(*[data])
        self._write_buffer()

    def draw_rect(self, x, y, w, h, color):
        self.draw_hline(*[x, y, w, color])
        self.draw_hline(*[x, ((y + h) - 1), w, color])
        self.draw_vline(*[x, y, h, color])
        self.draw_vline(*[((x + w) - 1), y, h, color])

    def draw_circle(self, x0, y0, r, color):
        f = (1 - r)
        ddF_x = 1
        ddF_y = -2 * r
        x = 0
        y = r
        self.draw_pixel(*[x0, (y0 + r), color])
        self.draw_pixel(*[x0, (y0 - r), color])
        self.draw_pixel(*[(x0 + r), y0, color])
        self.draw_pixel(*[(x0 - r), y0, color])
        while x < y:
            if f >= 0:

                dd_f_y += 2
                f += dd_f_y

            dd_f_x += 2
            f += dd_f_x
            self.draw_pixel(*[(x0 + x), (y0 + y), color])
            self.draw_pixel(*[(x0 - x), (y0 + y), color])
            self.draw_pixel(*[(x0 + x), (y0 - y), color])
            self.draw_pixel(*[(x0 - x), (y0 - y), color])
            self.draw_pixel(*[(x0 + y), (y0 + x), color])
            self.draw_pixel(*[(x0 - y), (y0 + x), color])
            self.draw_pixel(*[(x0 + y), (y0 - x), color])
            self.draw_pixel(*[(x0 - y), (y0 - x), color])

    def _draw_circle_helper(self, x0, y0, r, cornername, color):
        f = (1 - r)
        ddF_x = 1
        ddF_y = -2 * r
        x = 0
        y = r
        while x < y:
            if f >= 0:

                dd_f_y += 2
                f += dd_f_y

            dd_f_x += 2
            f += dd_f_x
            if cornername and 0x4:
                self.draw_pixel(*[(x0 + x), (y0 + y), color])
                self.draw_pixel(*[(x0 + y), (y0 + x), color])
            if cornername and 0x2:
                self.draw_pixel(*[(x0 + x), (y0 - y), color])
                self.draw_pixel(*[(x0 + y), (y0 - x), color])
            if cornername and 0x8:
                self.draw_pixel(*[(x0 - y), (y0 + x), color])
                self.draw_pixel(*[(x0 - x), (y0 + y), color])
            if cornername and 0x1:
                self.draw_pixel(*[(x0 - y), (y0 - x), color])
                self.draw_pixel(*[(x0 - x), (y0 - y), color])

    def fill_circle(self, x0, y0, r, color):
        self.draw_vline(*[x0, (y0 - r), (2 * r + 1), color])
        self._fill_circle_helper(*[x0, y0, r, 3, 0, color])

    def _fill_circle_helper(self, x0, y0, r, cornername, delta, color):
        f = (1 - r)
        ddF_x = 1
        ddF_y = -2 * r
        x = 0
        y = r
        while x < y:
            if f >= 0:

                dd_f_y += 2
                f += dd_f_y

            dd_f_x += 2
            f += dd_f_x
            if cornername and 0x1:
                self.draw_vline(*[(x0 + x), (y0 - y), ((2 * y + 1) + delta), color])
                self.draw_vline(*[(x0 + y), (y0 - x), ((2 * x + 1) + delta), color])
            if cornername and 0x2:
                self.draw_vline(*[(x0 - x), (y0 - y), ((2 * y + 1) + delta), color])
                self.draw_vline(*[(x0 - y), (y0 - x), ((2 * x + 1) + delta), color])

    def draw_round_rect(self, x, y, w, h, r, color):
        self.draw_hline(*[(x + r), y, (w - 2 * r), color])
        self.draw_hline(*[(x + r), ((y + h) - 1), (w - 2 * r), color])
        self.draw_vline(*[x, (y + r), (h - 2 * r), color])
        self.draw_vline(*[((x + w) - 1), (y + r), (h - 2 * r), color])
        self._draw_circle_helper(*[(x + r), (y + r), r, 1, color])
        self._draw_circle_helper(*[(((x + w) - r) - 1), (y + r), r, 2, color])
        self._draw_circle_helper(*[(((x + w) - r) - 1), (((y + h) - r) - 1), r, 4, color])
        self._draw_circle_helper(*[(x + r), (((y + h) - r) - 1), r, 8, color])

    def fill_round_rect(self, x, y, w, h, r, color):
        self.fill_rect(*[(x + r), y, (w - 2 * r), h, color])
        self._fill_circle_helper(*[(((x + w) - r) - 1), (y + r), r, 1, ((h - 2 * r) - 1), color])
        self._fill_circle_helper(*[(x + r), (y + r), r, 2, ((h - 2 * r) - 1), color])

    def draw_triangle(self, x0, y0, x1, y1, x2, y2, color):
        self.draw_line(*[x0, y0, x1, y1, color])
        self.draw_line(*[x1, y1, x2, y2, color])
        self.draw_line(*[x2, y2, x0, y0, color])

    def fill_triangle(self, x0, y0, x1, y1, x2, y2, color):
        a = None
        b = None
        y = None
        last = None
        if y0 > y1:
            y1 = [y0, y0 = y1][0]
            x1 = [x0, x0 = x1][0]
        if y1 > y2:
            y2 = [y1, y1 = y2][0]
            x2 = [x1, x1 = x2][0]
        if y0 > y1:
            y1 = [y0, y0 = y1][0]
            x1 = [x0, x0 = x1][0]
        if y0 == y2:
            a = b = x0
            if x1 < a:
                a = x1
            elif x1 > b:
                b = x1
            if x2 < a:
                a = x2
            elif x2 > b:
                b = x2
            self.draw_hline(*[a, y0, ((b - a) + 1), color])
            return
        dx01 = (x1 - x0)
        dy01 = (y1 - y0)
        dx02 = (x2 - x0)
        dy02 = (y2 - y0)
        dx12 = (x2 - x1)
        dy12 = (y2 - y1)
        sa = 0
        sb = 0
        if y1 == y2:
            last = y1
        else:
            last = (y1 - 1)
        # TODO: failed to generate FOR statement
        sa = dx12 * (y - y1)
        sb = dx02 * (y - y0)
        # TODO: failed to generate FOR statement

    def draw_vline(self, x, y, h, color):
        if x >= self.width or y >= self.height:
            return
        if ((y + h) - 1) >= self.height:
            h = (self.height - y)
        self.set_addr_window(*[x, y, x, ((y + h) - 1)])
        hi = color >> 8
        lo = color and 0xff
        data = []
        while :
            data.push(*[hi])
            data.push(*[lo])
        self.write_data(*[data])

    def draw_hline(self, x, y, w, color):
        if x >= self.width or y >= self.height:
            return
        if ((x + w) - 1) >= self.width:
            w = (self.width - x)
        self.set_addr_window(*[x, y, ((x + w) - 1), y])
        hi = color >> 8
        lo = color and 0xff
        data = []
        while :
            data.push(*[hi])
            data.push(*[lo])
        self.write_data(*[data])

    def draw_line(self, x0, y0, x1, y1, color):
        step = _math.abs(*[(y1 - y0)]) > _math.abs(*[(x1 - x0)])
        if step:
            y0 = [x0, x0 = y0][0]
            y1 = [x1, x1 = y1][0]
        if x0 > x1:
            x1 = [x0, x0 = x1][0]
            y1 = [y0, y0 = y1][0]
        dx = (x1 - x0)
        dy = _math.abs(*[(y1 - y0)])
        err = dx / 2
        ystep = 1 if y0 < y1 else -1
        # TODO: failed to generate FOR statement

    def draw_pixel(self, x, y, color):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return
        self.set_addr_window(*[x, y, (x + 1), (y + 1)])
        self.write_data(*[[color >> 8, color and 0xff]])

    def draw_char(self, x, y, ch, color, bg, size):
        size = size or 1
        if x >= self.width or y >= self.height or ((x + 6 * size) - 1) < 0 or ((y + 8 * size) - 1) < 0:
            return
        if color != bg:
            self.draw_char2(*[x, y, ch, color, bg, size])
            return
        c = ch.char_code_at(*[0])
        for i in range(0, 6, 1):
            line = 0 if i == 5 else font[(c * 5 + i)]
            for j in range(0, 8, 1):
                if line and 0x1:
                    if size == 1:
                        self.draw_pixel(*[(x + i), (y + j), color])
                    else:
                        self.fill_rect(*[(x + i * size), (y + j * size), size, size, color])
                elif bg != color:
                    if size == 1:
                        self.draw_pixel(*[(x + i), (y + j), bg])
                    else:
                        self.fill_rect(*[(x + i * size), (y + j * size), size, size, bg])
                line >>= 1

    def draw_char2(self, x, y, ch, color, bg, size):
        size = size or 1
        if x >= self.width or y >= self.height or ((x + 6 * size) - 1) < 0 or ((y + 8 * size) - 1) < 0:
            return
        pixels = [0] * 6 * 8 * size * size
        c = ch.char_code_at(*[0])
        for i in range(0, 6, 1):
            line = 0 if i == 5 else font[(c * 5 + i)]
            for j in range(0, 8, 1):
                cl = color if line and 0x1 else bg
                for w in range(0, size, 1):
                    for h in range(0, size, 1):
                        pixels[((i * 1 * size + w) + (j * 6 * size * size + h * 6 * size))] = cl
                line >>= 1
        self.raw_bound16(*[x, y, 6 * size, 8 * size, pixels])

    def raw_bound16(self, x, y, width, height, pixels):
        rgb = []
        pixels.for_each(*[lambda v: rgb.push(*[v and 0xff00 >> 8])])
        self.set_addr_window(*[x, y, ((x + width) - 1), ((y + height) - 1)])
        self._write_buffer(*[rgb])
        self._write_buffer()

    def draw_string(self, x, y, str, color, bg, size, wrap):
        size = size or 1
        for n in range(0, str.length, 1):
            c = str.char_at(*[n])
            if c == '\n':
                y += size * 8
                x = 0
            elif c == '\r':

            else:
                self.draw_char(*[x, y, c, color, bg, size])
                x += size * 6
                if wrap and x > (self.width - size * 6):
                    y += size * 8
                    x = 0
        return [x, y]

    def draw_context_bound(self, context, x0, y0, width, height, x1, y1, gray):
        x0 = x0 or 0
        y0 = y0 or 0
        width = width or context.canvas.client_width
        height = height or context.canvas.client_height
        x1 = x1 or 0
        y1 = y1 or 0
        gray = gray or False
        self.write(*[ST7735_COLMOD, [_st7735_18bit]])
        imageData = context.get_image_data(*[x0, y0, width, height]).data
        rgb = []
        for n in range(0, image_data.length, 4):
            r = image_data[(n + 0)]
            g = image_data[(n + 1)]
            b = image_data[(n + 2)]
            if not gray:
                rgb.push(*[r])
                rgb.push(*[g])
                rgb.push(*[b])
            else:
                gs = _math.round(*[((0.299 * r + 0.587 * g) + 0.114 * b)])
                rgb.push(*[gs])
                rgb.push(*[gs])
                rgb.push(*[gs])
        self.write(*[ST7735_COLMOD, [_st7735_18bit]])
        self.set_addr_window(*[x1, y1, ((x1 + width) - 1), ((y1 + height) - 1)])
        self._write_buffer(*[rgb])
        self._write_buffer()
        self.write(*[ST7735_COLMOD, [_st7735_16bit]])

    def draw_context(self, context, gray):
        gray = gray or False
        self.draw_context_bound(*[context, 0, 0, self.width, self.height, 0, 0, gray])

    def raw_bound(self, x, y, width, height, pixels):
        rgb = []
        pixels.for_each(*[lambda v: rgb.push(*[v and 0xff0000 >> 16])])
        self.write(*[ST7735_COLMOD, [_st7735_18bit]])
        self.set_addr_window(*[x, y, ((x + width) - 1), ((y + height) - 1)])
        self._write_buffer(*[rgb])
        self._write_buffer()
        self.write(*[ST7735_COLMOD, [_st7735_16bit]])

    def raw(self, pixels):
        self.raw(*[0, 0, self.width, self.height, pixels])

    def _set_preset_color(self):
        self.color = AttrDefault(bool, {'_alice_blue': 0xf7df, '_antique_white': 0xff5a, '_aqua': 0x07ff, '_aquamarine': 0x7ffa, '_azure': 0xf7ff, '_beige': 0xf7bb, '_bisque': 0xff38, '_black': 0x0000, '_blanched_almond': 0xff59, '_blue': 0x001f, '_blue_violet': 0x895c, '_brown': 0xa145, '_burly_wood': 0xddd0, '_cadet_blue': 0x5cf4, '_chartreuse': 0x7fe0, '_chocolate': 0xd343, '_coral': 0xfbea, '_cornflower_blue': 0x64bd, '_cornsilk': 0xffdb, '_crimson': 0xd8a7, '_cyan': 0x07ff, '_dark_blue': 0x0011, '_dark_cyan': 0x0451, '_dark_golden_rod': 0xbc21, '_dark_gray': 0xad55, '_dark_green': 0x0320, '_dark_khaki': 0xbdad, '_dark_magenta': 0x8811, '_dark_olive_green': 0x5345, '_dark_orange': 0xfc60, '_dark_orchid': 0x9999, '_dark_red': 0x8800, '_dark_salmon': 0xecaf, '_dark_sea_green': 0x8df1, '_dark_slate_blue': 0x49f1, '_dark_slate_gray': 0x2a69, '_dark_turquoise': 0x067a, '_dark_violet': 0x901a, '_deep_pink': 0xf8b2, '_deep_sky_blue': 0x05ff, '_dim_gray': 0x6b4d, '_dodger_blue': 0x1c9f, '_fire_brick': 0xb104, '_floral_white': 0xffde, '_forest_green': 0x2444, '_fuchsia': 0xf81f, '_gainsboro': 0xdefb, '_ghost_white': 0xffdf, '_gold': 0xfea0, '_golden_rod': 0xdd24, '_gray': 0x8410, '_green': 0x0400, '_green_yellow': 0xafe5, '_honey_dew': 0xf7fe, '_hot_pink': 0xfb56, '_indian_red': 0xcaeb, '_indigo': 0x4810, '_ivory': 0xfffe, '_khaki': 0xf731, '_lavender': 0xe73f, '_lavender_blush': 0xff9e, '_lawn_green': 0x7fe0, '_lemon_chiffon': 0xffd9, '_light_blue': 0xaedc, '_light_coral': 0xf410, '_light_cyan': 0xe7ff, '_light_golden_rod_yellow': 0xffda, '_light_gray': 0xd69a, '_light_green': 0x9772, '_light_pink': 0xfdb8, '_light_salmon': 0xfd0f, '_light_sea_green': 0x2595, '_light_sky_blue': 0x867f, '_light_slate_gray': 0x7453, '_light_steel_blue': 0xb63b, '_light_yellow': 0xfffc, '_lime': 0x07e0, '_lime_green': 0x3666, '_linen': 0xff9c, '_magenta': 0xf81f, '_maroon': 0x8000, '_medium_aqua_marine': 0x6675, '_medium_blue': 0x0019, '_medium_orchid': 0xbaba, '_medium_purple': 0x939b, '_medium_sea_green': 0x3d8e, '_medium_slate_blue': 0x7b5d, '_medium_spring_green': 0x07d3, '_medium_turquoise': 0x4e99, '_medium_violet_red': 0xc0b0, '_midnight_blue': 0x18ce, '_mint_cream': 0xf7ff, '_misty_rose': 0xff3c, '_moccasin': 0xff36, '_navajo_white': 0xfef5, '_navy': 0x0010, '_old_lace': 0xffbc, '_olive': 0x8400, '_olive_drab': 0x6c64, '_orange': 0xfd20, '_orange_red': 0xfa20, '_orchid': 0xdb9a, '_pale_golden_rod': 0xef55, '_pale_green': 0x9fd3, '_pale_turquoise': 0xaf7d, '_pale_violet_red': 0xdb92, '_papaya_whip': 0xff7a, '_peach_puff': 0xfed7, '_peru': 0xcc27, '_pink': 0xfe19, '_plum': 0xdd1b, '_powder_blue': 0xb71c, '_purple': 0x8010, '_rebecca_purple': 0x6193, '_red': 0xf800, '_rosy_brown': 0xbc71, '_royal_blue': 0x435c, '_saddle_brown': 0x8a22, '_salmon': 0xfc0e, '_sandy_brown': 0xf52c, '_sea_green': 0x2c4a, '_sea_shell': 0xffbd, '_sienna': 0xa285, '_silver': 0xc618, '_sky_blue': 0x867d, '_slate_blue': 0x6ad9, '_slate_gray': 0x7412, '_snow': 0xffdf, '_spring_green': 0x07ef, '_steel_blue': 0x4416, '_tan': 0xd5b1, '_teal': 0x0410, '_thistle': 0xddfb, '_tomato': 0xfb08, '_turquoise': 0x471a, '_violet': 0xec1d, '_wheat': 0xf6f6, '_white': 0xffff, '_white_smoke': 0xf7be, '_yellow': 0xffe0, '_yellow_green': 0x9e66})