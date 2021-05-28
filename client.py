import sys
import os
from local.offloading import send_frame
from local.client_end import Client
import logging
import common
import argparse

from tools.transfer_files_tool import transfer_array_and_str

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--video', help='input video file')
    parser.add_argument('-i', '--image', help='input image')
    args = parser.parse_args()
    video_file = args.video
    image_file = args.image

    while True:
        try:
            input_file = video_file
            assert input_file is not None
            assert os.path.isfile(input_file)
            file_type = input("please input file type: image or video\n")
            assert file_type is not None
            assert file_type == "image" or file_type == "video"
            service_type = input("please input file type: image classification or object detection\n")
            assert service_type is not None
            assert service_type == "image classification" or service_type == "object detection"
        except AssertionError:
            print("please input again:")
        else:
            break

    file_type = common.IMAGE_TYPE
    service_type = common.IMAGE_CLASSIFICATION
    client = Client(input_file, file_type, service_type)
    while True:
        # get frames
        frame = client.reader.read_file()
        # preprocessing frames
        if frame is None:
            client.info.store()
            print("service comes over!")
            exit()

        msg_dict, selected_model = client.decision_engine.get_decision_result(client.info.info_list[-1][0], client.info.info_list[-1][1])
        frame = client.preprocessing.pre_process_image(frame, **msg_dict)
        file_size = sys.getsizeof(frame)
        # transmission
        result_dict, total_service_delay, arrive_transfer_server_time = send_frame(client.picture_url, frame, selected_model)
        if service_type == "image classification":

            result = result_dict["prediction"]
            net_speed = file_size / arrive_transfer_server_time
            client.info.append(total_service_delay, net_speed)
            print(result)
        else:
            frame_shape = tuple(int(s) for s in result_dict["frame_shape"][1:-1].split(","))
            frame_handled = transfer_array_and_str(result_dict["result"], 'down').reshape(frame_shape)
            client.local_store.store_image(frame_handled)
            net_speed = file_size / arrive_transfer_server_time
            client.info.append(total_service_delay, net_speed)
