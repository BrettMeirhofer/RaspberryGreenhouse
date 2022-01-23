import os
import datetime


def take_picture():
    current_time = datetime.datetime.now().strftime("%Y%m%d%H%M")
    command = "ffmpeg -f v4l2 -video_size 1280x720 -i /dev/video0 -frames 1 {}.jpg".format(current_time)
    os.system(command)


if __name__ == '__main__':
    take_picture()
