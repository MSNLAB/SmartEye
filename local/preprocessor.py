from PIL import Image
import os
import subprocess
import numpy as np
from loguru import logger


class PreProcessor:
    def __init__(self, frame):
        self.frame = frame

    def preprocess(self, **msg_dict):
        """
        Preprocess the video frame based on the resolution decided by the decision engine
        msg_dict: image size, support 100×100 poxels 500x500 pixels
        """
        frame = Image.fromarray(self.frame)
        frame = frame.resize(tuple(msg_dict['image_size']), Image.ANTIALIAS)
        frame = np.asarray(frame)
        return frame

    def preprocess_by_qp(self, frame, qp):
        """Change the image quality

        :param frame: image frame, ndarray
        :param qp: the quality number which image changes to
        :return: image frame, ndarray
        """

        image = Image.fromarray(frame)
        # temporary_store = read_config("store-folder", "temporary_store")
        temporary_store = os.path.join(os.path.dirname(__file__), "../info_store/temporary_file")
        file_path = os.path.join(temporary_store, 'temporary.jpg')
        image.save(file_path, quality=qp)
        img = Image.open(file_path)
        frame = np.array(img)
        return frame

    def preprocess_video(self, input_file, **b_r_dict):
        """Adjust the input_file's resolution and bitrate according to the parameter b_r_tuple

        :param input_file: video file path
        :param b_r_dict: the max b_r_tuple value of video transfered to
        :return: file save path
        """
        folder_path = os.path.dirname(input_file)
        file_pre_name = os.path.basename(input_file).split(".")[0]
        file_suffix = os.path.basename(input_file).split(".")[1]
        file_path = (folder_path + "/" + file_pre_name + "_" + b_r_dict['bitrate']
                     + "_" + b_r_dict['resolution'] + "." + file_suffix)
        cmd = ("ffmpeg -i " + input_file + " -vf scale=" + b_r_dict['resolution']
               + " -b:v " + b_r_dict['bitrate'] + " -maxrate " + b_r_dict['bitrate']
               + " -bufsize 2M " + file_path)

        subprocess.Popen(cmd)
        return file_path
