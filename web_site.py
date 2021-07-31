import datetime
import io
import tempfile
import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, flash, send_file, redirect, url_for
import flyer
from os.path import join, dirname, realpath

__author__ = 'Konstantin Kovalev'

# -*- coding: utf-8 -*-
load_dotenv()

config = {
    "DEBUG": True,
    "SECRET_KEY": os.getenv('SECRET_KEY', '.env'),
    "UPLOAD_FOLDER": join(dirname(realpath(__file__)), 'uploads/'),
    "ALLOWED_EXTENSIONS": {'png', 'jpg', 'jpeg'},
    "MAX_CONTENT_LENGTH": 1024 * 1024
}

application = Flask(__name__)
application.config.from_mapping(config)


def allowed_file(filename):
    return filename.split('.')[-1].lower() in config['ALLOWED_EXTENSIONS']


@application.route("/", methods=["GET"])
def index():
    return render_template("ork.html")


@application.route("/ork", methods=["POST"])
def orks():
    op_data = dict(
        find_man=request.form['find_man'].upper(),
        op_name=request.form['op_name'],
        year_old=request.form['year_old'],
        your_telephone=request.form['your_telephone'],
        op_location=request.form['op_location'],
        lost_conditional=request.form['lost_conditional'],
        sign=request.form['sign_txt'],
        was_dressed=request.form['was_dressed_txt'],
        have_with=request.form['have_with'],
        special_sign=request.form['special_sign'],
        attention=request.form['attention'],
        op_photo=request.files['op_photo']
    )

    if op_data['op_photo'].filename == '':
        flash('Фото не выбрано')
        return redirect('/')

    if not (op_data['op_photo'] and allowed_file(op_data['op_photo'].filename)):
        flash('File not specified')
        return redirect(url_for('/'))

    with tempfile.NamedTemporaryFile() as tmp_file:
        op_data['op_photo'].save(tmp_file)
        tmp_file.flush()
        photo = tmp_file.name

        flyer.background_generator = flyer.BackgroundGenerator(flyer.lynx_bg_size, 'white')

        flyer.lynx_ork = flyer.BackgroundLynx(flyer.lynx_size_border, flyer.com_color_border, flyer.ork_font_arial,
                                              flyer.font_arial_bold, flyer.lynx_font_black, flyer.lynx_text_border_top,
                                              flyer.lynx_text_border_foot, flyer.lynx_op_photo_size,
                                              photo, flyer.source_dir_op_lynx,
                                              flyer.lynx_margin_border, flyer.lynx_color_text_border,
                                              op_data['your_telephone'], flyer.lynx_text_inform)
        flyer.lynx_ork.border_lynx_ork()
        flyer.lynx_ork.text_border_top_ork()
        flyer.lynx_ork.text_border_foot_ork()
        flyer.lynx_ork.tel_number_ork()
        flyer.lynx_ork.text_inform_ork()
        flyer.lynx_ork.photo_ork()

        flyer.lynx_ork_leaflet = flyer.LeafletLynx(op_data['op_location'], flyer.size_year_loc_fnt_lynx,
                                                   op_data['year_old'], op_data['op_name'], op_data['find_man'])
        flyer.lynx_ork_leaflet.help_text_ork()
        flyer.lynx_ork_leaflet.name_surname_text_ork()
        flyer.lynx_ork_leaflet.op_year_text_text_ork()
        flyer.lynx_ork_leaflet.op_location_text_text_ork()

        flyer.lynx_ork_description = flyer.DescriptionLeafletLynx(op_data['sign'], op_data['was_dressed'],
                                                                  op_data['have_with'], op_data['special_sign'],
                                                                  op_data['attention'],
                                                                  flyer.lynx_width_line_conditional_text,
                                                                  flyer.lynx_conditional_font_size,
                                                                  op_data['lost_conditional'])

        pillow_image = flyer.lynx_ork_description.attention_ork_test_if_empty()

        img_byte_arr = io.BytesIO()
        pillow_image.save(img_byte_arr, format='JPEG')
        img_byte_arr.seek(0)
        date_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%s")
        return send_file(img_byte_arr, mimetype="image/jpeg", as_attachment=True, download_name=f'orientirovka-{date_str}.jpeg')


if __name__ == "__main__":
    application.run(host='0.0.0.0')
