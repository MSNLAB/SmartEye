import os
import time
import subprocess

save_folder_path = '../'


def extract_frames(input_file):
    """
    Extract 1 frame every 5 frames
    :param input_file: video path
    :return: pictures stored path
    """
    folder_pre_path = os.path.dirname(input_file)
    folder_name = os.path.basename(input_file).split(".")[0]
    folder_path = folder_pre_path + "/" + folder_name
    if not os.path.isdir(folder_path):
        os.mkdir(folder_path, 777)
        # pass
    cmd = ("ffmpeg -i " + input_file + " -r 5 -f image2 "
           + folder_path + "/" + folder_name + "_%05d.jpg")
    p = subprocess.Popen(cmd)
    return folder_path


def compose_video(picture_folder_path, video_path):
    """
    compose pictures to a video
    :param: picture_folder_path: picture path
    :param: video_path: video save path
    :return: video save path
    """
    folder_pre_path = os.path.dirname(video_path)
    folder_name = os.path.basename(video_path).split(".")[0]
    suffix = os.path.basename(video_path).split(".")[1]
    video_name = folder_pre_path + folder_name + '_processed' + suffix
    # audio or not
    cmd = "ffmpeg -loop 1 -f image2 -i " + picture_folder_path + " -vcodec libx264 -r 5 -t 10 " + video_name
    subprocess.Popen(cmd)
    return video_name

