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
    parser.add_argument('-v', '--video', help='input video file path')
    parser.add_argument('-i', '--image', help='input image path')
    parser.add_argument('-s', '--serv', help='service type: classification | detection')
    args = parser.parse_args()
    video_file = args.video
    image_file = args.image

    input_file = None
    file_type = None
    if video_file is not None:
        input_file = video_file
        file_type = common.VIDEO_TYPE
    elif image_file is not None:
        input_file = image_file
        file_type = common.IMAGE_TYPE
    else:
        print("Error: no matched file type")
        sys.exit()
    if os.path.isfile(input_file) is False:
        print("Error: file not exists")
        sys.exit()

    serv_type = None
    if args.serv == "classification":
        serv_type = common.IMAGE_CLASSIFICATION
    elif args.serv == "detection":
        serv_type = common.OBJECT_DETECTION

    client = Client(input_file, file_type, serv_type)
    while True:
        # read a frame
        frame = client.reader.read_frame()
        # preprocessing frames
        if frame is None:
            client.info.store()
            print("service comes over!")
            sys.exit()

        msg_dict, selected_model = client.decision_engine.get_decision_result(client.info.info_list[-1][0], client.info.info_list[-1][1])
        frame = client.preprocessing.pre_process_image(frame, **msg_dict)
        file_size = sys.getsizeof(frame)
        # transmission
        result_dict, total_service_delay, arrive_transfer_server_time = send_frame(client.picture_url, frame, selected_model)
        if serv_type == common.IMAGE_CLASSIFICATION:

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
