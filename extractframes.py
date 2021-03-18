import os
import time



def extract_frames(input_file):
    """
    Extract 1 frame every 5 frames
    :param input_file: video path
    :return: pictures stored path
    """

    folder_pre_path = os.path.dirname(input_file)
    folder_name = os.path.basename(input_file).split(".")[0]
    folder_path = folder_pre_path + "\\" + folder_name
    # print(folder_pre_path)
    # print(folder_name)
    print(folder_path)
    if not os.path.isdir(folder_path):
        # print(1)
        os.mkdir(folder_path, 777)
        # pass

    cmd = ("ffmpeg -i " + input_file + " -r 5 -f image2 " +
          folder_path + "\\" + folder_name + "-%05d.jpg")

    os.system(cmd)
    return folder_path

if __name__ == '__main__':

    t1 = time.time()
    extract_frames("D:\\Ubuntu_1804.2019.522.0_x64\\rootfs\home\wxz\Documents\\video2edge\85652500-1-192.mp4")
    t2 = time.time()
    print('%s' % (t2 - t1))