import exifinfo

from os import path

from PIL import Image, ImageOps, ImageDraw, ImageFont

class Pipeline:
    """
    Handles creating an image with a border and text of the image's info
    """
    def __init__(self, filename=None):
        """
        Initialize pipeline object

        Args:
            filename: The image's filename

        """
        self.set_filename(filename)
        
    def set_filename(self, filename):
        """
        Sets a new image filename

        Args:
            filename: The image's filename
        """
        if not (path.exists(filename) and path.isfile(filename)):
            raise Exception("file does not exist or is not a file")
        self.filename = filename

    def process(self, info):
        """
        Process the image data and metadata to generate a new image with a border and text of the image's info

        Args:
            info: The config.Handler object

        """
        if self.filename == None:
            raise Exception("filename is not set")
        image = Image.open(self.filename)
        exif = image.getexif()
        infostr = exifinfo.parse_exif_data(exif, info.get_metadata())
        img_with_border = create_img_with_border(image, info.get_background())
        add_text(img_with_border, infostr, info.get_font())
        save_file(self.filename, img_with_border)


def create_img_with_border(img, info):
    """
    Creates a new image with a surrounding border.

    Args:
        img: The Image object
        info: The info object to pull background config from

    Returns:
        A new Image object
    """
    return ImageOps.expand(img, border=info["pixels"], fill=info["color"])

def get_color(color):
    """
    Get the tuple value for the given color
    Currently only supports white and black

    Args:
        color: The color string (ex "white")
    
    Returns:
        Tuple value for RGB
    """
    if color == "white":
        return (255, 255, 255)
    else:
        return (0, 0, 0)

def add_text(img, text, info):
    """
    Add text to the bottom center of the image.

    Args:
        img: The Image object
        text: The text to add
        info: The info object to pull font config from

    """
    # size is (width, height)
    size = img.size
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(info["ttf_file"], info["point"])
    text_width = font.getsize(text)[0]
    x_offset = 0.5 * size[0] - (text_width * 0.5)
    y_offset = info["y_offset_pct"] * size[1]
    draw.text((x_offset, size[1] - y_offset), text, get_color(info["color"]), font=font)

def save_file(filename, img):
    """
    Save the given image.

    Args:
        filename: The filename to save the image as
        img: The Image object
    
    """
    filename = filename.split(".")
    newname = ".".join(filename[:-1])
    img.save(newname + "-edited." + filename[-1])