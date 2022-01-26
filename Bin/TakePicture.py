import os
import datetime
import time
import SendData
import GreenhouseFuncs as GHF
import pytz


def take_picture():
    logger = GHF.create_logger("TakePicture")
    current_time = datetime.datetime.now(tz=pytz.UTC).strftime("%Y%m%d%H%M")
    target_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Images", current_time + ".png")
    command = "ffmpeg -f v4l2 -video_size 1280x720 -i /dev/video0 -frames 1 " + target_path
    os.system(command)
    time.sleep(1)
    SendData.send_image_data(open(target_path, "rb"))


if __name__ == '__main__':
    take_picture()
