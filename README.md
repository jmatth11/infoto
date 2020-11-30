# infoto
A script to automate generating a JPEG photo with a border and the specified metadata in text on the image.

__This project is still a work in progress__

Example:

Original Image
![](references/DSC_1331.jpg)

After ran through script
![](references/DSC_1331-edited.jpg)

## Contents

- [Requirements](#requirements)
- [Running the Script](#running-the-script)
- [JSON Config File](#json-config-file)
    - [metadata](#metadata)
        - [order](#order)
        - [pre/postfix](#pre/postfix)
    - [font](#font)
        - [y_offset_pct](#y_offset_pct)
    - [background](#background)
    - [image](#image)
- [References](#references)

Very much WIP

## Requirements

- python3.5
- Pillow 7.2
- TTF font file; check [References](#references) to find downloads for TTF font files

## Running the Script

The script requires 1 argument

Script Argument:
- JSON config file
- debug flag; requires the character 'y' to work

Example running the script:
```bash
$ python main.py info.json [y]
```

## JSON Config File

The JSON config file currently supports these top level fields:
- `metadata`; Specify the EXIF fields you want to pull and the info associated with it
- `font`; Specify the font info
- `background`: Specify the background info
- `image`; Specify the image filename

### metadata

Supported fields are any supported EXIF tags. These tags can be found [here](https://exiftool.org/TagNames/EXIF.html).
The link is also in the [References](#references) section.

Supported fields within these Tag objects are:
- `prefix`; a string to be concatenated to the beginning of the value
- `postfix`; a string to be concatenated to the end of the value
- `order`; The order in the formatted string when added to the image. This number is [0, N) where N is the number of fields you have in metadata.

```json
"metadata": {
    "ExposureTime": {
        "prefix": "",
        "postfix": " SEC",
        "order": 0
    },
    "FNumber": {
        "prefix": "F",
        "postfix": "",
        "order": 1
    }
}
```

#### order

The `order` property must be within the [0, N) range otherwise the script will error out.

#### pre/postfix

The `pre/postfix` properties are whitespace senstive. So this value `"F"` will show up like so `F22` while this value `"F "` will show up like so `F 22`.

### font

Supported fields in the font object:
- `point`; The font point value; a number
- `ttf_file`; The TTF filename
- `color`; check [References](#references) for color options
- `y_offset_pct`; This is the y_offset percentage value to be used when setting the text.

```json
"font": {
    "point": 50,
    "ttf_file": "fonts/MonospaceTypewriter.ttf",
    "color": "black",
    "y_offset_pct": 0.1
}
```

#### y_offset_pct

This value is used like so:
```python
offset = y_offset_pct * image_height
y_offset = image_height - offset
```

This offsets the value from the bottom of the image. So a `0.1` value means the text will be `0.1%` from the bottom of the image.

### background

Supported fields in the background object:
- `color`; check [References](#references) for color options
- `pixels`; number of pixels to add as a border around the image

```json
"background": {
    "color": "white",
    "pixels": 300
}
```

### image

This is just a string value of the image filename.

```json
"image": "path/to/filename"
```

---

## References

Color option references here:
- https://pillow.readthedocs.io/en/stable/reference/ImageColor.html#color-names

EXIF Tags listed here:
- https://exiftool.org/TagNames/EXIF.html

TTF font files can be downloaded at these links:
- https://all-free-download.com/font/
- https://ttfonts.net/
