import config
import imageutil
import sys

def process_image(info):
    """
    Process the given image and output a new image with a border and text of the image's info

    Args:
        info: The config.Handler object
    """
    pipeline = imageutil.Pipeline(info.get_image())
    pipeline.process(info)
    
if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("An info.json file is required as an argument.")
        exit()
    try:
        config_info = config.create_handler(sys.argv[1])
        process_image(config_info)
    except Exception as err:
        import traceback
        if len(sys.argv) == 3:
            if sys.argv[2] == "y":
                traceback.print_exc()
        print(err)
