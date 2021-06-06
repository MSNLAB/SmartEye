import sys
import os
from multiprocessing.managers import BaseManager

import common
import argparse
import time
from local import globals
from local.decision_engine import DecisionEngine
from local.local_info import update_local_utilization
from local.local_processor import LocalProcessor
from local.local_store import LocalStore
from frontend_server.offloading import send_frame
from local.preprocessor import PreProcessor
from local.proxy import Proxy
from local.system_info import SysInfo
from local.video_reader import VideoReader
from tools.read_config import read_config
from tools.transfer_files_tool import transfer_array_and_str
import multiprocessing
from multiprocessing import Pool


def seal(queue, local_processor, decision_engine, preprocessor, sys_info, local_store, serv_type):

    picture_url = read_config("transfer-url", "picture_url")
    frame = queue.get()
    decide_processor = decision_engine.get_processor_decision(globals.local_cpu_usage.value, globals.local_memory_usage.value)
    if decide_processor == common.LOCAL:
        selected_model = decision_engine.get_decision()

        t1 = time.time()
        result = local_processor.process(frame, selected_model)
        t2 = time.time()
        processing_delay = t2 - t1
        if serv_type == common.IMAGE_CLASSIFICATION:
            sys_info.append(t1, processing_delay)
            print(result)
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
        bandwidth = file_size / arrive_transfer_server_time
        print(result_dict.keys())
        if serv_type == common.IMAGE_CLASSIFICATION:
            result = result_dict["prediction"]
            sys_info.append(start_time, processing_delay, bandwidth)
            print(result)
        elif serv_type == common.OBJECT_DETECTION:
            frame_shape = tuple(int(s) for s in result_dict["frame_shape"][1:-1].split(","))
            frame_handled = transfer_array_and_str(result_dict["result"], 'down').reshape(frame_shape)
            local_store.store_image(frame_handled)
            sys_info.append(start_time, processing_delay, bandwidth)
        else:
            print("Error: no specified service type")


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
    # video_file_url = read_config("transfer-url", "video_file_url")
    # store_type = args.store
    # if store_type is not None:
    #     store_type = int(args.store)
    globals.init()
    # subprocess, update the cpu_usage and memory_usage every ten seconds
    p = multiprocessing.Process(
        target=update_local_utilization,
        args=(globals.local_cpu_usage, globals.local_memory_usage)
    )
    p.start()

    reader = VideoReader(input_file)
    queue = multiprocessing.Manager().Queue(10)
    pool = Pool(5, globals.init, ())

    BaseManager.register('LocalProcessor', LocalProcessor)   # Proxy
    BaseManager.register('DecisionEngine', DecisionEngine)
    BaseManager.register('PreProcessor', PreProcessor)
    BaseManager.register('SysInfo', SysInfo, Proxy)
    BaseManager.register('LocalStore', LocalStore)
    manager = BaseManager()
    manager.start()
    local_processor = manager.LocalProcessor(input_file, serv_type)
    # print(local_processor.input_file)
    decision_engine = manager.DecisionEngine(file_type, serv_type)
    preprocessor = manager.PreProcessor()
    sys_info = manager.SysInfo()
    # print(sys_info)
    local_store = manager.LocalStore()

    while True:
        # get frames
        frame = reader.read_frame()
        # preprocessing frames
        if frame is None:
            sys_info.store()
            p.terminate()
            print("service comes over!")
            exit()
        queue.put(frame)
        args = [queue, local_processor, decision_engine, preprocessor, sys_info, local_store, serv_type]
        pool.apply(seal, args=args)
    pool.close()
    pool.join()


