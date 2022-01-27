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
    for x in range(3):
        target_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Images", current_time + str(x) + ".png")
        command = "ffmpeg -f v4l2 -video_size 1280x720 -i /dev/video0 -frames 1 " + target_path
        os.system(command)
        time.sleep(1)
    time.sleep(1)
    SendData.send_image_data(open(target_path, "rb"))


if __name__ == '__main__':
    take_picture()
