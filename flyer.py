import textwrap
import re
from PIL import Image, ImageDraw, ImageFont
import time

__author__ = 'Konstantin Kovalev'

# -*- coding: utf-8 -*-

start_time = time.time()

lynx_bg_size = (1280, 905)
lynx_size_border = 50
fnt_size_border = lynx_size_border - 10
lynx_op_photo_size = (417, 555)
lynx_margin_border = 20


""" for font """
ork_font_arial = 'font/arial.ttf'
font_arial_bold = 'font/ofont.ru_Arial.ttf'
font_arial_black = 'font/6426.ttf'
lynx_font_black = 'font/myriadpro-blackcond.ttf'
size_year_loc_fnt_lynx = 34
lynx_conditional_font_size = 29
lynx_width_line_conditional_text = 48

lynx_text_border_top = 'Внимание!'.upper()  # text for header on border
lynx_text_border_foot = 'Внимание!'.upper()  # text for footer on border
lynx_color_text_border = 'white'
com_color_border = '#A67200'
lynx_tel_number = '8(831)28-38-200 или 102'  # telephone number for footer
lynx_text_inform = 'Всех кто обладает информацией ' \
                   'просим сообщить по телефону:'  # text for footer under telephone number


find_man = 'Помогите найти ребенка'.upper()

op_name_lynx = 'Сибирякова Александра Владимировна'  # Name of lost
year_old = '1976'
# op_old_lynx = f'({year_old} г.р.)'  # Years old of lost
op_location = 'Арзамасский р-он., c. Ковакса'

# Sign text
lynx_lost_conditional = '25.06.2021 г.Ночью ушел из дома пр. Краснознаменного артелирийского полка и пропал'
lynx_sign = 'плотного телосложения, рост 165 см., волосы светлые короткие, глаза зелено-карие.'
# sign_txt = f'Приметы: {sign}\n'
lynx_was_dressed = 'кепка цвета хаки ( бежево-зеленая),' \
                   ' белая футболка-поло с воротником, черные шорты, черные кроссовки.'
# was_dressed_txt = f'Был одет: {was_dressed}\n'
lynx_have_with = 'мобильный телефон, ключи от дома.'
# have_with_txt = f'При себе имел: {have_with}\n'
lynx_special_sign = 'татуировки на левой руке от запястья до локтя.'
# special_sign_txt = f'Особые приметы: {special_sign}\n'
lynx_attention = ''
count = 0

source_dir_op_lynx = 'image/oppic/'  # path for images
op_images_lynx = 'image/oppic/photo_2018-11-20_07-43-08.jpg'  # list with filename in directory
# op_images_lynx = os.listdir(source_dir_op_lynx)  # list with filename in directory


class BackgroundGenerator:
    # Generate background & declare technical function
    def __init__(self, bg_size, bg_color):
        self.bg_size = bg_size
        self.bg_color = bg_color
        self.bg_canvas = Image.new('RGB', (self.bg_size[0], self.bg_size[1]), color=bg_color)  # Create canvas
        self.draw_bg = ImageDraw.Draw(self.bg_canvas)  # Draw background

    # Draw border on leaflet
    def draw_bg_border(self, border_color, border_width):
        self.draw_bg.rectangle(((0, 0), self.bg_size), outline=border_color, width=border_width)
        return self.bg_canvas

    def font_image(self, fnt, fnt_size):
        fnt_img = ImageFont.truetype(fnt, size=fnt_size)
        return fnt_img

    def text_size(self, txt, fnt):
        txt_sz = self.draw_bg.textsize(txt, font=fnt)
        return txt_sz

    def font_size_generator(self, txt, font, size_w, size_h=10000):
        font_size = 1
        fnt = self.font_image(font, font_size)
        while fnt.getsize(txt)[0] < size_w and fnt.getsize(txt)[1] < size_h:
            font_size += 1
            fnt = self.font_image(font, font_size)
        return font_size

    # Find center text
    def center_text(self, txt, first_width, font_text):
        w, h = self.draw_bg.textsize(txt, font=font_text)
        center_position = ((first_width - w) / 2)
        return center_position

    def draw_txt(self, coordinates, txt, fnt, color):
        self.draw_bg.text(coordinates, txt, font=fnt, fill=color)
        return self.bg_canvas


class BackgroundLynx:
    # Create background
    def __init__(self, size_border, color_border, font_arial, font_bold, font_black, text_border_top,
                 text_border_foot, op_photo_size, op_images, source_dir_oppic, margin_border,
                 color_text_border, tel_number, text_inform):
        self.size_border = size_border
        self.color_border = color_border
        self.font_arial = font_arial
        self.font_bold = font_bold
        self.text_border_foot = text_border_foot
        self.text_border_top = text_border_top
        self.op_photo_size = op_photo_size
        self.source_dir_oppic = source_dir_oppic
        self.photo = op_images
        self.font_size_border = self.size_border - 10
        self.margin_border = margin_border
        self.tel_number = tel_number
        self.text_inform = text_inform
        self.font_black = font_black
        self.color_text_border = color_text_border
        self.coords_text_border_top = ((background_generator.bg_size[0] - self._text_border_top_size()[0]) / 2,
                                       (self.size_border - self._text_border_top_size()[1]) / 2)
        self.coords_text_border_footer = ((background_generator.bg_size[0] - self._text_border_footer_size()[0]) / 2,
                                          (background_generator.bg_size[1] - self.size_border))
        self.coords_photo_margin_w = (self.op_photo_size[0] + self.size_border + self.margin_border)
        self.size_photo_to_ending_w = (background_generator.bg_size[0] - self.size_border * 2 -
                                       self.coords_photo_margin_w)
        self.coords_tel_number = (self.coords_photo_margin_w,
                                  background_generator.bg_size[1] - self.size_border - self.margin_border -
                                  self._tel_number_text_size()[1])
        self.coords_text_inform = (self.coords_photo_margin_w,
                                   self.coords_tel_number[1] - self._text_inform_text_size()[1])
        self.coord_op_photo_h = (background_generator.bg_size[1] - (self._photo_size()[1] - 1) - self.size_border)

    def border_lynx_ork(self):
        border = background_generator.draw_bg_border(self.color_border, self.size_border)
        return border

    def _op_sort_image(self):
        with Image.open(self.photo) as p:
            resize_op_photo = p.resize(self.op_photo_size)
            return resize_op_photo

    def _photo_size(self):
        return self._op_sort_image().size

    # Text for border
    def _font_for_border(self):
        font = background_generator.font_image(self.font_bold, self.font_size_border)
        return font

    def _text_border_top_size(self):
        text = background_generator.text_size(self.text_border_top, self._font_for_border())
        return text

    def _text_border_footer_size(self):
        text = background_generator.text_size(self.text_border_foot, self._font_for_border())
        return text

    def text_border_top_ork(self):
        ork = background_generator.draw_txt(self.coords_text_border_top, self.text_border_top,
                                            self._font_for_border(), self.color_text_border)
        return ork

    def text_border_foot_ork(self):
        ork = background_generator.draw_txt(self.coords_text_border_footer, self.text_border_foot,
                                            self._font_for_border(), self.color_text_border)
        return ork

    # Telephone number
    def _font_size_tel_number(self):  # Create font size for telephone number
        fnt_sz = background_generator.font_size_generator(self.tel_number, self.font_black, self.size_photo_to_ending_w)
        return fnt_sz

    def _font_tel_number(self):  # Create font setting
        font = background_generator.font_image(self.font_black, self._font_size_tel_number())
        return font

    def _tel_number_text_size(self):  # Create size text for telephone number
        txt_size = background_generator.text_size(self.tel_number, self._font_tel_number())
        return txt_size

    def tel_number_ork(self):  # Insert text on leaflet
        ork = background_generator.draw_txt(self.coords_tel_number, self.tel_number, self._font_tel_number(), 'black')
        return ork

    # Text inform
    def _font_size_text_inform(self):
        fnt_sz = background_generator.font_size_generator(self.text_inform, self.font_bold, self.size_photo_to_ending_w)
        return fnt_sz

    def _font_text_inform(self):
        font = background_generator.font_image(self.font_bold, self._font_size_text_inform())
        return font

    def _text_inform_text_size(self):
        text_size = background_generator.text_size(self.text_inform, self._font_text_inform())
        return text_size

    def text_inform_ork(self):
        ork = background_generator.draw_txt(self.coords_text_inform,
                                            self.text_inform, self._font_text_inform(), 'black')
        return ork

    # Insert photo wanted people on background
    def photo_ork(self):
        ork = background_generator.bg_canvas.paste(self._op_sort_image(), (self.size_border, self.coord_op_photo_h))
        return ork


class LeafletLynx:

    def __init__(self, location, size_year_loc_font, op_old, op_name, big_red_text):
        self.big_red_text = big_red_text
        self.op_name = op_name
        self.op_old = op_old
        self.op_old_full = f'({self.op_old} г.р.)'  # Years old of lost
        self.size_year_loc_fnt = size_year_loc_font
        self.location = location
        self.size_inside_border_and_margin_w = (background_generator.bg_size[0] - (lynx_ork.size_border * 2) -
                                                (lynx_ork.margin_border * 2))
        self.size_op_name_h = (background_generator.bg_size[1] - lynx_ork.op_photo_size[1]) - \
                              ((lynx_ork.size_border * 7) - self._help_text_text_size()[1])
        self.coords_help_text = ((self._help_text_center_search()), (lynx_ork.size_border + lynx_ork.margin_border))
        self.coords_name_surname_text = ((self._name_surname_text_center_search()),
                                         (lynx_ork.size_border + lynx_ork.margin_border * 2 +
                                         self._help_text_text_size()[1]))
        self.coords_year_text = (lynx_ork.coords_photo_margin_w, lynx_ork.coord_op_photo_h)
        self.coords_location_text = (background_generator.bg_size[0] - self.op_location_text_text_size()[0] -
                                     lynx_ork.size_border - lynx_ork.margin_border, lynx_ork.coord_op_photo_h)

    # Big top red text
    def _font_size_help_text(self):  # return font size
        fnt_sz = background_generator.font_size_generator(self.big_red_text, lynx_ork.font_black,
                                                          self.size_inside_border_and_margin_w)
        return fnt_sz

    def _font_help_text(self):
        font = background_generator.font_image(lynx_ork.font_black, self._font_size_help_text())
        return font

    def _help_text_text_size(self):
        text_size = background_generator.text_size(self.big_red_text, self._font_help_text())
        return text_size

    def _help_text_center_search(self):
        center = background_generator.center_text(self.big_red_text, background_generator.bg_size[0],
                                                  self._font_help_text())
        return int(center)

    def help_text_ork(self):
        ork = background_generator.draw_txt(self.coords_help_text, self.big_red_text, self._font_help_text(), 'red')
        return ork

    # Add name lost man in leaflet
    def _name_surname_text_font_size(self):  # return font size
        fnt_sz = background_generator.font_size_generator(self.op_name, lynx_ork.font_black,
                                                          self.size_inside_border_and_margin_w, self.size_op_name_h)
        return fnt_sz

    def _name_surname_text_font(self):
        font = background_generator.font_image(lynx_ork.font_black, self._name_surname_text_font_size())
        return font

    def _name_surname_text_text_size(self):
        text_size = background_generator.text_size(self.op_name, self._name_surname_text_font())
        return text_size

    def _name_surname_text_center_search(self):
        center = background_generator.center_text(self.op_name, background_generator.bg_size[0],
                                                  self._name_surname_text_font())
        return int(center)

    def name_surname_text_ork(self):
        ork = background_generator.draw_txt(self.coords_name_surname_text, self.op_name,
                                            self._name_surname_text_font(), 'black')
        return ork

    # Add year in leaflet
    def _op_year_location_text_font(self):
        font = background_generator.font_image(lynx_ork.font_bold, self.size_year_loc_fnt)
        return font

    def _op_year_text_text_size(self):
        text_size = background_generator.text_size(self.op_old_full, self.size_year_loc_fnt)
        return text_size

    def op_year_text_text_ork(self):
        ork = background_generator.draw_txt(self.coords_year_text, self.op_old_full,
                                            self._op_year_location_text_font(), 'black')
        return ork

    # Add location in leaflet
    def op_location_text_text_size(self):
        text_size = background_generator.text_size(self.location, self._op_year_location_text_font())
        return text_size

    def op_location_text_text_ork(self):
        ork = background_generator.draw_txt(self.coords_location_text,
                                            self.location, self._op_year_location_text_font(), 'black')
        return ork


class DescriptionLeafletLynx:
    # Add description, attention text
    def __init__(self, sign, was_dressed, have_with, special_sign, attention_text, width_line_conditional_text,
                 conditional_font_size, lost_conditional):
        self.sign = sign
        self.sign_txt = f'Приметы: {self.sign}\n'
        self.was_dressed = was_dressed
        self.was_dressed_txt = f'Был одет: {self.was_dressed}\n'
        self.have_with = have_with
        self.have_with_txt = f'При себе имел: {self.have_with}\n'
        self.special_sign = special_sign
        self.special_sign_txt = f'Особые приметы: {self.special_sign}\n'
        self.width_line_conditional_text = width_line_conditional_text
        self.lost_conditional = lost_conditional
        self.list_desc = [self.sign, self.was_dressed, self.have_with, self.special_sign]
        self.list_full_desc = [self.sign_txt, self.was_dressed_txt, self.have_with_txt, self.special_sign_txt]
        self.count = 0
        self.attention_text = attention_text
        self.size_area_attention_text_h = 50
        self.conditional_font_size = conditional_font_size
        self.coords_detail_text_h = (background_generator.bg_size[1] - lynx_ork.op_photo_size[1]) + \
                                    (lynx_ork_leaflet.op_location_text_text_size()[1]) - \
                                    (lynx_ork.size_border / 2)  # Generate info about position

        self.coords_attention_text_area = (background_generator.bg_size[0] - lynx_ork.coords_photo_margin_w) -\
                                          (lynx_ork.size_border * 2)  # This var for generate center position

    # Splitting text into lines
    def text_sep(self, text, width_line, coords_w, coords_h, font_whith_size, font_highlight, color):
        for line in textwrap.wrap(text, width=width_line):
            find_select_text = re.match(r'^\D+:', line)
            if find_select_text:
                crop_line = line[len(find_select_text.group(0)):]
                background_generator.draw_bg.text((coords_w, coords_h), find_select_text.group(0), font=font_highlight,
                                                  fill=color)
                background_generator.draw_bg.text((coords_w + font_highlight.getsize(find_select_text.group(0))[0],
                                                   coords_h), crop_line, font=font_whith_size, fill=color)
                coords_h += font_whith_size.getsize(line)[1]
            else:
                background_generator.draw_bg.text((coords_w, coords_h), line, font=font_whith_size, fill=color)
                coords_h += font_whith_size.getsize(line)[1]
        return background_generator.bg_canvas, coords_h

    # Add conditional text
    def _lost_conditional_text_font(self):
        font = background_generator.font_image(lynx_ork.font_arial, self.conditional_font_size)
        return font

    def _highlight_description_text_font(self):
        font = background_generator.font_image(lynx_ork.font_bold, self.conditional_font_size)
        return font

    def _lost_conditional_text_highlight_text_font(self):
        font = background_generator.font_image(lynx_ork.font_black, self.conditional_font_size)
        return font

    def _lost_conditional_text_sep_ork(self):
        ork_text_sep = self.text_sep(self.lost_conditional,
                                     self.width_line_conditional_text,
                                     lynx_ork.coords_photo_margin_w,
                                     self.coords_detail_text_h,
                                     self._lost_conditional_text_font(),
                                     self._highlight_description_text_font(),
                                     'black')
        return ork_text_sep

    # Add description text
    def _selection_not_empty_text(self):
        description_text_list = []
        for text, add_txt in zip(self.list_desc, self.list_full_desc):
            if len(text) > 0:
                description_text_list.append(add_txt)
        return description_text_list

    def add_description_text(self):
        global ork_sign
        for desc in self._selection_not_empty_text():
            if self.count == 0:
                heigh_position, back = (self._lost_conditional_text_sep_ork()[1] + lynx_ork.size_border / 2),\
                                       (self._lost_conditional_text_sep_ork())
            else:
                heigh_position, back = ork_sign[1], lynx_ork.coords_photo_margin_w
            ork_sign = self.text_sep(desc,
                                     self.width_line_conditional_text,
                                     lynx_ork.coords_photo_margin_w,
                                     heigh_position,
                                     self._lost_conditional_text_font(),
                                     self._highlight_description_text_font(),
                                     color='black')
            self.count += 1
        return ork_sign

    # Create and add attention text
    def _attention_text_font_size(self):  # return font size
        fnt_sz = background_generator.font_size_generator(self.attention_text, lynx_ork.font_bold,
                                                          lynx_ork.size_photo_to_ending_w,
                                                          self.size_area_attention_text_h)
        return fnt_sz

    def _attention_text_font(self):
        font = background_generator.font_image(lynx_ork.font_bold, self._attention_text_font_size())
        return font

    def _attention_text_center_search(self):
        center = background_generator.center_text(self.attention_text, self.coords_attention_text_area,
                                                  self._attention_text_font())
        return int(center)

    def _attention_text_ork(self):
        ork = background_generator.draw_txt(self.coords_attention_text, self.attention_text,
                                            self._attention_text_font(), 'red')
        return ork

    def attention_ork_test_if_empty(self):
        if len(self.attention_text) > 0:
            self.coords_attention_text = (lynx_ork.coords_photo_margin_w + self._attention_text_center_search(),
                                          ((lynx_ork.coords_text_inform[1] + self.add_description_text()[1] -
                                            lynx_ork.size_border) / 2))  # This var for define position on flyer

            return self._attention_text_ork()
        else:
            self.coords_attention_text = (lynx_ork.coords_photo_margin_w,
                                          ((lynx_ork.coords_text_inform[1] + self.add_description_text()[1] -
                                            lynx_ork.size_border) / 2))  # This var for define position on flyer
            return self._lost_conditional_text_sep_ork()[0]

if __name__ == '__main__':

    background_generator = BackgroundGenerator(lynx_bg_size, 'white')

    lynx_ork = BackgroundLynx(lynx_size_border, com_color_border, ork_font_arial, font_arial_bold, lynx_font_black,
                              lynx_text_border_top, lynx_text_border_foot, lynx_op_photo_size, op_images_lynx,
                              source_dir_op_lynx, lynx_margin_border, lynx_color_text_border, lynx_tel_number,
                              lynx_text_inform)

    lynx_ork.border_lynx_ork()
    lynx_ork.text_border_top_ork()
    lynx_ork.text_border_foot_ork()
    lynx_ork.tel_number_ork()
    lynx_ork.text_inform_ork()
    lynx_ork.photo_ork()

    lynx_ork_leaflet = LeafletLynx(op_location, size_year_loc_fnt_lynx,
                                   year_old, op_name_lynx, find_man)

    lynx_ork_leaflet.help_text_ork()
    lynx_ork_leaflet.name_surname_text_ork()
    lynx_ork_leaflet.op_year_text_text_ork()
    lynx_ork_leaflet.op_location_text_text_ork()

    lynx_ork_description = DescriptionLeafletLynx(lynx_sign, lynx_was_dressed, lynx_have_with, lynx_special_sign,
                                                  lynx_attention, lynx_width_line_conditional_text,
                                                  lynx_conditional_font_size, lynx_lost_conditional)

    lynx_ork_description.attention_ork_test_if_empty().show()
    print("--- %s seconds ---" % (time.time() - start_time))

