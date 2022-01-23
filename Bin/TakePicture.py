import os
import datetime


def take_picture():
    current_time = datetime.datetime.now().strftime("%Y%m%d%H%M")
    target_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Images", current_time + ".png")
    command = "ffmpeg -f v4l2 -video_size 1280x720 -i /dev/video0 -frames 1 " + target_path
    os.system(command)


if __name__ == '__main__':
    take_picture()