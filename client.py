import sys
import os
from concurrent.futures.thread import ThreadPoolExecutor

import common
import argparse
import time
import threading
from local.decision_engine import DecisionEngine
from local.local_info import update_local_utilization
from local.local_processor import LocalProcessor, load_model
from local.local_store import LocalStore
from frontend_server.offloading import send_frame
from local.preprocessor import PreProcessor
from local.sys_info import SysInfo
from local.video_reader import VideoReader
from tools.read_config import read_config
from tools.transfer_files_tool import transfer_array_and_str
import multiprocessing
from loguru import logger

global loaded_model
global selected_model
global msg_dict


def local_worker(serv_type, local_queue, sys_info, local_store):
    local_processor = LocalProcessor()
    while True:
        frame = local_queue.get()
        t_start = time.time()
        result = local_processor.process(frame, selected_model, loaded_model)
        t_end = time.time()
        processing_delay = t_end - t_start
        if serv_type == common.IMAGE_CLASSIFICATION:
            sys_info.append(t_start, processing_delay)
            logger.info("local:" + result)
        elif serv_type == common.OBJECT_DETECTION:
            sys_info.append(t_end, processing_delay)
            local_store.store_image(result)
            logger.info("local object detection works well!")
        else:
            logger.error("no specified service type")


def offload_worker(serv_type, frame, msg_dict, sys_info, local_store):
    preprocessor = PreProcessor()
    image_url = read_config("transfer-url", "image_url")

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
    parser.add_argument('-c', '--camera', help="input camera type, "
                                               "'rtsp' for Webcam, "
                                               "'local' for local camera")
    parser.add_argument('-s', '--serv', type=int, help="input service demand,"
                                                       "'3' for IMAGE_CLASSIFICATION," 
                                                       "'4' for OBJECT_DETECTION", required=True)
    parser.add_argument('-i', '--interval', type=int, help="interval between reading two frames in ms", required=True)
    args = parser.parse_args()

    file_type = common.IMAGE_TYPE
    serv_type = args.serv
    INTERVAL = args.interval / 1000.0   # change into seconds

    input_file = args.file
    if input_file is not None:
        if not os.path.isfile(input_file):
            logger.error("input video file does not exist")
            sys.exit()

    camera_type = None
    if args.camera is not None:
        camera_type = args.camera

    if input_file is None and camera_type is None:
        logger.error("input video file and camera type cannot be both None")
        sys.exit()

    if input_file is not None and camera_type is not None:
        logger.error("use either video file or camera")
        sys.exit()

    logger.add("log/client_{time}.log", level="INFO")
    loaded_model = load_model()

    reader = VideoReader(input_file, camera_type)
    decision_engine = DecisionEngine(file_type, serv_type)
    local_store = LocalStore()
    sys_info = SysInfo()

    local_queue = multiprocessing.Queue(int(read_config("some-number", "queue_length")))

    # start the thread pool for processing offloading requests
    executor = ThreadPoolExecutor(max_workers=2)
    # start the process for local inference
    local_processor = multiprocessing.Process(target=local_worker,
                                              args=(serv_type, local_queue, sys_info, local_store))
    local_processor.start()

    while True:
        # read frames from video file or camera
        frame = reader.read_frame()
        if frame is None:
            logger.error("service comes over!")
            sys.exit()

        t_start = time.time()
        location, msg_dict, selected_model = decision_engine.get_result(sys_info)
        logger.debug(location)

        if location == common.LOCAL:
            local_queue.put(frame)
        elif location == common.OFFLOAD:
            task1 = executor.submit(offload_worker, serv_type, frame, msg_dict, sys_info, local_store)

        # sleep until the duration of INTERVAL seconds has passed
        t_end = time.time()
        if t_end - t_start < INTERVAL:
            dur = INTERVAL - (t_end - t_start)
            time.sleep(dur)



