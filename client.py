import sys
import os
from multiprocessing.managers import BaseManager

import common
import argparse
import time
from local import globals
from local.decision_engine import DecisionEngine
from local.local_info import update_local_utilization
from local.local_processor import LocalProcessor, load_model
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


def worker(
        queue, local_processor, preprocessor, sys_info, local_store,
        serv_type, flag, msg_dict, selected_model, loaded_model
):

    image_url = read_config("transfer-url", "image_url")
    frame = queue.get()
    # logger.debug("msg_dict:"+str(id(msg_dict)))
    if flag == common.LOCAL:
        t1 = time.time()
        result = local_processor.process(frame, selected_model, loaded_model)
        t2 = time.time()
        processing_delay = t2 - t1
        if serv_type == common.IMAGE_CLASSIFICATION:
            sys_info.append(t1, processing_delay)
            logger.info("local:"+result)
        elif serv_type == common.OBJECT_DETECTION:
            sys_info.append(t1, processing_delay)
            local_store.store_image(result)
            logger.info("local object detection works well!")
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
                logger.info("offload:"+result)
            elif serv_type == common.OBJECT_DETECTION:
                frame_shape = tuple(int(s) for s in result_dict["frame_shape"][1:-1].split(","))
                frame_handled = transfer_array_and_str(result_dict["result"], 'down').reshape(frame_shape)
                local_store.store_image(frame_handled)
                sys_info.append(start_time, processing_delay, bandwidth)
                logger.info("offload object detection works well!")
            else:
                logger.error("Seal error: no specified service type!")


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='input video file')
    parser.add_argument('-c', '--camera', help="input camera type, 'rtsp' for Webcam, 'local' for local camera")
    parser.add_argument('-s', '--serv', type=int, help="input service demand, '3' for IMAGE_CLASSIFICATION," 
                                                       "'4' for OBJECT_DETECTION", required=True)
    parser.add_argument('-i', '--interval', type=int, help="read frame interval between two frames", required=True)
    # parser.add_argument('-ST', '--store', help="input store type demand, "
    #                                            "'0' for IMAGE, '1' for VIDEO, IMAGE By default")
    args = parser.parse_args()

    file_type = common.IMAGE_TYPE
    interval = args.interval
    input_file = args.file
    if input_file is not None:
        if not os.path.isfile(input_file):
            logger.error("Error: file not exists")
            sys.exit()

    camera_type = None
    if args.camera is not None:
        camera_type = args.camera

    serv_type = args.serv

    if input_file is None and camera_type is None:
        logger.error("file and camera can not be None at the same time!")
        sys.exit()

    if input_file is not None and camera_type is not None:
        logger.error("Both file and camera can not have value at the same time!")
        sys.exit()

    # store_type = ""
    # video_file_url = read_config("transfer-url", "video_file_url")
    # store_type = args.store
    # if store_type is not None:
    #     store_type = int(args.store)

    globals.init()
    logger.add("log/client_{time}.log", level="INFO")
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
    model_manager = multiprocessing.Manager()
    loaded_model = model_manager.dict(load_model())

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

    while True:
        # get frames
        if camera_type is not None:
            frame = reader.read_frame()
            time.sleep(interval)
        elif input_file is not None:
            for i in range(interval):
                image = reader.read_frame()
                if i == 0:
                    frame = image

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
        logger.debug(selected_model)
        queue.put(frame)

        args = [
            queue, local_processor, preprocessor, sys_info, local_store,
            serv_type, flag, msg_dict, selected_model, loaded_model
        ]

        for i in range(int(read_config("some-number", "subprocess_number"))):
            pool.apply_async(worker, args=args)
    pool.close()
    pool.join()

