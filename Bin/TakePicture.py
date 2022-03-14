import os
import datetime
import time
import SendData
import GreenhouseFuncs as GHF
import pytz


# ffmpeg seems to need a light and dark calibration image before a good image is produced
# Three pictures are taken while only the 3rd is uploaded
def take_picture():
    logger = GHF.create_logger("TakePicture")
    current_time = datetime.datetime.now(tz=pytz.UTC).strftime("%Y%m%d%H%M")
    target_path = ""
    config_dict = GHF.open_config_dict("Config.json")
    for camera in config_dict["cams"]:
        for x in range(3):
            file_name = camera["name"] + current_time + str(x) + ".png"
            target_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Images", file_name)
            command = "ffmpeg -f v4l2 -video_size 1280x720 -i {} -frames 1 {}".format(camera["sys"], target_path)
            os.system(command)
            time.sleep(1)
        time.sleep(1)
        SendData.send_image_data(open(target_path, "rb"), params={"cam": camera["id"]})


if __name__ == '__main__':
    take_picture()
