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
    parser.add_argument('-i', '--file', help='input file')
    # parser.add_argument('-F', '--filetype', help="input file type, '0' for IMAGE, '1' for VIDEO")
    parser.add_argument('-s', '--serv', help="input service demand, '3' for IMAGE_CLASSIFICATION," 
                                             "'4' for OBJECT_DETECTION")
    # parser.add_argument('-ST', '--store', help="input store type demand, "
    #                                            "'0' for IMAGE, '1' for VIDEO, IMAGE By default")
    args = parser.parse_args()

    file_type = common.IMAGE_TYPE

    input_file = None
    if args.file is not None:
        input_file = args.file
    else:
        print("Error: no matched file type")
        sys.exit()
    if not os.path.isfile(input_file):
        print("Error: file not exists")
        sys.exit()

    serv_type = None
    if args.serv is not None:
        serv_type = int(args.serv)

    # store_type = args.store
    # if store_type is not None:
    #     store_type = int(args.store)

    client = Client(input_file, file_type, serv_type)

    while True:
        # get frames
        frame = client.reader.read_frame()
        # preprocessing frames
        if frame is None:
            client.info.store()
            print("service comes over!")
            exit()

        msg_dict, selected_model = client.decision_engine.get_decision()
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
