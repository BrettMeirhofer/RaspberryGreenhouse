import os
import datetime
import time
import SendData
import GreenhouseFuncs as GHF
import pytz


# ffmpeg seems to need a light and dark calibration image before a good image is produced
# Three pictures are taken while only the 3rd is uploaded
def take_picture():
    logger = GHF.create_logger("Stream")
    config_dict = GHF.open_config_dict("Config.json")
    for camera in config_dict["cams"]:
        file_name = camera["name"] + ".png"
        target_path = os.path.join(os.path.dirname(__file__), "static", "img", file_name)
        command = "ffmpeg -f v4l2 -video_size 1280x720 -i {} -frames 1 {}".format(camera["sys"], target_path)
        os.system(command)
        time.sleep(.1)


if __name__ == '__main__':
    take_picture()
