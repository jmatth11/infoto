from PIL.ExifTags import TAGS
from PIL.TiffImagePlugin import IFDRational

def get_exif_value(exif, field):
    """
    Grabs the value for the given field name

    Args:
        exif: the exif data
        field: the field name
    
    Returns:
        The value for the given field name
    """
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

def format_shutter_speed(rat):
    """
    Get the shutter speed in the correct format

    Args:
        rat: The IFDRational object for shutter speed

    Returns:
        Formatted string
    """
    # TODO handle point values for 1.3, 1.5, 2.5
    if not isinstance(rat, IFDRational):
        return val
    if rat.denominator == 1:
        return "{}".format(rat.numerator)
    return "{}/{}".format(rat.numerator, rat.denominator)

def format_IFDRationals(rat):
    """
    Get the correct formatted string for a IFDRational object

    Args:
        rat: The IFDRational object

    Returns:
        Formatted string
    """
    if not isinstance(rat, IFDRational):
        return val
    # IFDRational allows for 0 denominator so check for it
    if rat.denominator == 0:
        return rat.numerator
    val = rat.numerator / rat.denominator
    # only show integer part if there is no significant fractional part
    if val.is_integer():
        return int(val)
    return val
    

def handle_format(name, val, fixes):
    """
    Get the formatted string for an EXIF value

    Args:
        name: The EXIF tag name
        val: The EXIF value
        fixes: The pre/post fixes to be added to the formatting
    
    Returns:
        Formatted string
    """
    # handle exposure time as a special case 
    if name == "ExposureTime":
        val = format_shutter_speed(val)
    elif isinstance(val, IFDRational):
        val = format_IFDRationals(val)
    
    return "{}{}{}".format(fixes["prefix"], val, fixes["postfix"])


def parse_exif_data(exif, info):
    """
    Get the formatted string of all wanted EXIF data.

    Args:
        exif: The EXIF data
        info: The info dictionary of all metadata fields wanted to display

    Returns:
        Formatted string
    """
    # create list allocated to length of number of fields
    output = [None] * len(info)
    for name in info:
        fixes = info[name]
        field_value = get_exif_value(exif, name)
        if field_value is None:
            print("no value set for metadata field: {}", name)
            continue
        index = fixes["order"]
        if index >= len(output) or index < 0:
            print("{}'s order must be between 0 and the number of info items you have. Current order value: {}".format(name, order))
            exit()
        output[index] = handle_format(name, field_value, fixes)
    return ' | '.join(output)