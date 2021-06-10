import cv2
from PIL import Image
import os
import subprocess
import numpy as np
# from matplotlib import image as matimg
# from tools.read_config import read_config


class PreProcessor:
    """The preprocess execution of image data.

    Inpute video frames or directly a video file,
    this class will transfer them to different resolution, qp etc.
    """
    def preprocess_image(self, frame, **msg_dict):
        """Preprocess image.

        According to the image_size decided by Decision Engine,
        this function adjusts the image size of which will be sent to the server.

        :param msg_dict: image size, support 100×100 poxels， 500x500 pixels
        :param frame: images which needs to be adjust
        :return: file save path
        """
        assert frame is not None
        image = Image.fromarray(frame)
        result_image = image.resize(tuple(msg_dict['image_size']), Image.ANTIALIAS)
        frame = np.asarray(image)
        return frame

    def preprocess_by_qp(self, frame, qp):
        """Change the image quality

        :param frame: image frame, ndarray
        :param qp: the quality number which image changes to
        :return: image frame, ndarray
        """
        assert frame is not None
        assert qp is not None
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


if __name__ == '__main__':

    # image_size_adjust((500, 500), './gile1.jpg')
    pass
