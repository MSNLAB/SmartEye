import sys
import os
import common
import argparse
import time
from local import globals
from local.decision_engine import DecisionEngine
from local.local_processor import LocalProcessor
from local.local_store import LocalStore
from frontend_server.offloading import send_frame
from local.preprocessor import PreProcessor
from local.system_info import SysInfo
from local.video_reader import VideoReader
from tools.read_config import read_config
from tools.transfer_files_tool import transfer_array_and_str

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--file', help='input video file')
    parser.add_argument('-s', '--serv', help="input service demand, '3' for IMAGE_CLASSIFICATION," 
                                             "'4' for OBJECT_DETECTION")
    # parser.add_argument('-ST', '--store', help="input store type demand, "
    #                                            "'0' for IMAGE, '1' for VIDEO, IMAGE By default")
    args = parser.parse_args()

    input_file = None
    file_type = common.IMAGE_TYPE

    if args.file is not None:
        input_file = args.file
    else:
        print("Error: no input video file")
        sys.exit()
    if not os.path.isfile(input_file):
        print("Error: file not exists")
        sys.exit()

    serv_type = None
    if args.serv is not None:
        serv_type = int(args.serv)
    # store_type = ""

    picture_url = read_config("transfer-url", "picture_url")
    video_file_url = read_config("transfer-url", "video_file_url")
    # store_type = args.store
    # if store_type is not None:
    #     store_type = int(args.store)
    globals.init()
    local_processor = LocalProcessor(input_file, serv_type)
    reader = VideoReader(input_file)
    decision_engine = DecisionEngine(file_type, serv_type)
    preprocessor = PreProcessor()
    sys_info = SysInfo()
    local_store = LocalStore()

    while True:
        # get frames
        frame = reader.read_frame()
        # preprocessing frames
        if frame is None:
            sys_info.store()
            print("service comes over!")
            exit()

        decide_processor = decision_engine.get_processor_decision()

        if decide_processor == common.LOCAL:
            selected_model = decision_engine.get_decision()
            print(selected_model)
            t1 = time.time()
            result = local_processor.process(frame, selected_model)
            t2 = time.time()
            processing_delay = t2 - t1
            if serv_type == common.IMAGE_CLASSIFICATION:
                print(result)
                sys_info.append(t1, processing_delay)
            elif serv_type == common.OBJECT_DETECTION:
                # frame_shape = frame_handled.shape
                local_store.store_image(result)
                sys_info.append(t1, processing_delay)
            else:
                print("Error: no specified service type")

        elif decide_processor == common.OFFLOAD:

            msg_dict, selected_model = decision_engine.get_decision(sys_info)
            frame = preprocessor.preprocess_image(frame, **msg_dict)
            file_size = sys.getsizeof(frame)
            # send the video frame to the server
            result_dict, start_time, processing_delay, arrive_transfer_server_time = \
                send_frame(picture_url, frame, selected_model)

            if serv_type == common.IMAGE_CLASSIFICATION:
                result = result_dict["prediction"]
                bandwidth = file_size / arrive_transfer_server_time
                sys_info.append(start_time, processing_delay, bandwidth)
                print(result)
            elif serv_type == common.OBJECT_DETECTION:
                frame_shape = tuple(int(s) for s in result_dict["frame_shape"][1:-1].split(","))
                frame_handled = transfer_array_and_str(result_dict["result"], 'down').reshape(frame_shape)
                local_store.store_image(frame_handled)
                bandwidth = file_size / arrive_transfer_server_time
                sys_info.append(start_time, processing_delay, bandwidth)
            else:
                print("Error: no specified service type")
