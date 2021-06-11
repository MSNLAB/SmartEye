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
from loguru import logger


# logger.remove(handler_id=None)
logger.add("client.log", level="TRACE")


def worker(queue, local_processor, preprocessor, sys_info, local_store, serv_type, flag, msg_dict, selected_model):

    image_url = read_config("transfer-url", "image_url")
    frame = queue.get()

    if flag == common.LOCAL:
        t1 = time.time()
        result = local_processor.process(frame, selected_model)
        t2 = time.time()
        processing_delay = t2 - t1
        logger.debug(processing_delay)
        if serv_type == common.IMAGE_CLASSIFICATION:
            sys_info.append(t1, processing_delay)
            print(result)
        elif serv_type == common.OBJECT_DETECTION:
            sys_info.append(t1, processing_delay)
            local_store.store_image(result)
        else:
            logger.error("Seal error: no specified service type!")

    elif flag == common.OFFLOAD:

        frame = preprocessor.preprocess_image(frame, **msg_dict)
        file_size = sys.getsizeof(frame)
        # send the video frame to the server
        try:
            result_dict, start_time, processing_delay, arrive_transfer_server_time = \
                send_frame(image_url, frame, selected_model)
        except Exception as err:
            logger.exception("return back err!")
        else:
            bandwidth = file_size / arrive_transfer_server_time
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
                logger.error("Seal error: no specified service type!")


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='input video file')
    parser.add_argument('-c', '--camera', help="input camera type, '9' for REAL_CAMERA, '10' for VIRTUAL_CAMERA")
    parser.add_argument('-s', '--serv', help="input service demand, '3' for IMAGE_CLASSIFICATION," 
                                             "'4' for OBJECT_DETECTION")
    # parser.add_argument('-ST', '--store', help="input store type demand, "
    #                                            "'0' for IMAGE, '1' for VIDEO, IMAGE By default")

    args = parser.parse_args()

    file_type = common.IMAGE_TYPE

    input_file = args.file
    if input_file is not None:
        if not os.path.isfile(input_file):
            logger.error("Error: file not exists")
            sys.exit()

    camera_type = None
    if args.camera is not None:
        camera_type = int(args.camera)

    serv_type = None
    if args.serv is not None:
        serv_type = int(args.serv)
    else:
        logger.error("Error: server type can not be None!")
        sys.exit()

    if input_file is None and camera_type is None:
        logger.error("file and camera can not be None at the same time!")
        sys.exit()

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

    reader = VideoReader(input_file, camera_type)
    decision_engine = DecisionEngine(file_type, serv_type)

    queue = multiprocessing.Manager().Queue(int(read_config("some-number", "queue_length")))
    pool = Pool(int(read_config("some-number", "subprocess_number")), globals.init, ())

    BaseManager.register('LocalProcessor', LocalProcessor)
    BaseManager.register('PreProcessor', PreProcessor)
    BaseManager.register('SysInfo', SysInfo, Proxy)
    BaseManager.register('LocalStore', LocalStore)
    manager = BaseManager()
    manager.start()

    local_processor = manager.LocalProcessor(input_file, serv_type)
    preprocessor = manager.PreProcessor()
    sys_info = manager.SysInfo()
    local_store = manager.LocalStore()

    frame_interval = int(read_config("read-frequency", "frame_interval"))
    while True:
        # get frames
        for i in range(frame_interval):
            if i == 0:
                frame = reader.read_frame()
        # preprocessing frames
        if frame is None:
            sys_info.store()
            p.terminate()
            print("service comes over!")
            exit()
        flag, msg_dict, selected_model = decision_engine.get_result(
            globals.local_cpu_usage.value,
            globals.local_memory_usage.value,
            sys_info
        )
        queue.put(frame)
        args = [queue, local_processor, preprocessor, sys_info, local_store, serv_type, flag, msg_dict, selected_model]
        pool.apply_async(worker, args=args)
    pool.close()
    pool.join()

