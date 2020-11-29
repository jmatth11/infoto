import json
import sys

from os import path

from PIL import Image, ImageOps, ImageDraw, ImageFont
from PIL.ExifTags import TAGS

def get_field(exif, field):
    for k in exif:
        tag_name = TAGS.get(k)
        v = exif.get(k)
        if isinstance(tag_name, str):
            if isinstance(v, bytes):
                try:
                    v = v.decode()
                except:
                    print("could not decode value for field: {}".format(tag_name))
        if tag_name == field:
            return v

def shutter_speed_format(field_value):
    return "{}/{}".format(field_value.numerator, field_value.denominator)

def handle_format(name, field_value, fixes):
    if name == "ExposureTime":
        return "{}{}{}".format(fixes["prefix"], shutter_speed_format(field_value), fixes["postfix"])
    else:
        return "{}{}{}".format(fixes["prefix"], field_value, fixes["postfix"])

def parse_exif_data(exifdata, info):
    output = [None] * len(info)
    for name in info:
        fixes = info[name]
        field_value = get_field(exifdata, name)
        if field_value is None:
            print("no value set for metadata field: {}", name)
            continue
        index = fixes["order"]
        if index >= len(output) or index < 0:
            print("{}'s order must be between 0 and the number of info items you have. Current order value: {}".format(name, order))
            exit()
        output[fixes["order"]] = handle_format(name, field_value, fixes)
    return ' | '.join(output)

def create_img_with_border(img, info):
    return ImageOps.expand(img, border=300, fill=info["color"])

def get_color(color):
    if color == "white":
        return (255, 255, 255)
    else:
        return (0, 0, 0)

def add_text(img, infostr, info):
    # size is (width, height)
    size = img.size
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(info["ttf_file"], info["point"])
    text_width = font.getsize(infostr)[0]
    x_offset = 0.5 * size[0] - (text_width * 0.5)
    y_offset = 0.04 * size[1]
    draw.text((x_offset, size[1] - y_offset), infostr, get_color(info["color"]), font=font)

def save_file(filename, img):
    filename = filename.split(".")
    newname = ".".join(filename[:-1])
    img.save(newname + "-edited." + filename[-1])

def export_info_image(image_file, info):
    if not (path.exists(image_file) and path.isfile(image_file)):
        print("could not find the given image file")
        exit()
    image = Image.open(image_file)
    exifdata = image.getexif()
    infostr = parse_exif_data(exifdata, info["metadata"])
    img_with_border = create_img_with_border(image, info["background"])
    add_text(img_with_border, infostr, info["font"])
    save_file(image_file, img_with_border)


def read_info_file(file_name):
    if not (path.exists(file_name) and path.isfile(file_name)):
        print("could not find the given info file")
        exit()
    with open(file_name) as f:
        data = json.load(f)
    return data

if __name__ == "__main__":
    if len(sys.argv) <= 2:
        print("A JPEG image file and info.json file are required as arguments.")
        exit()
    info = read_info_file(sys.argv[2])
    export_info_image(sys.argv[1], info)
