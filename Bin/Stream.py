import os
import time
from helper import GreenhouseFuncs as GHF


# Takes a single picture
def take_picture():
    logger = GHF.create_logger("Stream")
    config_dict = GHF.open_config_dict("Config.json")
    for camera in config_dict["cams"]:
        file_name = camera["name"] + ".png"
        target_path = os.path.join(os.path.dirname(__file__), "static", "img", file_name)
        overwrite = ""
        if os.path.exists(target_path):
            overwrite = " -y"
        command = "ffmpeg{} -f v4l2 -video_size 1280x720 -i {} -frames 1 {}".format(overwrite, camera["sys"], target_path)
        os.system(command)
        time.sleep(.1)


if __name__ == '__main__':
    take_picture()

