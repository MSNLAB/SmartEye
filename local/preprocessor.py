from PIL import Image
import os
import random
import numpy as np


def video_frame_resize(frame, new_height):

    frame = Image.fromarray(frame)
    hpercent = (new_height / float(frame.size[1]))
    wsize = int((float(frame.size[0]) * float(hpercent)))
    frame = frame.resize((wsize, new_height), Image.ANTIALIAS)
    frame = np.asarray(frame)
    return frame


def video_frame_change_qp(frame, qp):
    """Change the image quality"""
    image = Image.fromarray(frame)
    temporary_store = os.path.join(os.path.dirname(__file__), "../../Downloads/SmartEye/info_store/temporary_file")
    n = random.randrange(0, 1000)
    file_path = os.path.join(temporary_store, 'temporary_' + str(n) + '.jpg')
    image.save(file_path, quality=qp)
    img = Image.open(file_path)
    frame = np.array(img)
    os.remove(file_path)
    return frame


def preprocess(task):
    """Preprocess the video frame based on the resolution decided by the decision engine"""
    if task.new_size is not None:
        task.frame = video_frame_resize(task.frame, task.new_size)

    if task.new_qp is not None:
        task.frame = video_frame_change_qp(task.frame, task.new_qp)

    return task


