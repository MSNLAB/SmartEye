import sys
import os
import queue
import threading
from concurrent.futures.thread import ThreadPoolExecutor
import common
import argparse
import time
from local.decision_engine import DecisionEngine
from model_manager.model_cache import load_model
from local.sys_info import SysInfo
from local.video_reader import VideoReader
from loguru import logger
from worker import local_worker, offload_worker, Task, id_gen


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-f', '--file', help="input video file or local camera")
    group.add_argument('-r', '--rtsp', help="RTSP camera", action='store_true')
    parser.add_argument('-s', '--serv', type=int, help="input service demand,"
                                                       "'3' for IMAGE_CLASSIFICATION," 
                                                       "'4' for OBJECT_DETECTION", required=True)
    parser.add_argument('-i', '--interval', type=int, help="interval between reading two frames in ms", required=True)
    args = parser.parse_args()

    logger.add("log/client_{time}.log", level="INFO")

    file_type = common.IMAGE_TYPE
    serv_type = args.serv
    INTERVAL = args.interval / 1000.0   # change into seconds

    input_file = args.file
    if input_file is not None:
        if os.path.isfile(input_file) is False and input_file.isdigit() is False:
            logger.error("input video file or local camera does not exist")
            sys.exit()
        elif input_file.isdigit():
            input_file = int(input_file)

    if input_file is None and args.rtsp is False:
        logger.error("should either select video file or RTSP camera")
        sys.exit()

    common.loaded_model = load_model()

    reader = VideoReader(input_file, args.rtsp)
    decision_engine = DecisionEngine(file_type, serv_type)
    common.sys_info = SysInfo()

    # start the thread pool for processing offloading requests
    executor = ThreadPoolExecutor(max_workers=2)
    # the queue for local processing task
    task_queue = queue.Queue()
    # start the process for local inference
    local_processor = threading.Thread(target=local_worker, args=(task_queue, common.sys_info))
    local_processor.start()

    while True:
        # read frames from video file or camera
        frame = reader.read_frame()
        if frame is None:
            logger.error("service comes over!")
            sys.exit()

        t_start = time.time()
        common.sys_info.update_local_utilization()
        location, msg_dict, selected_model = decision_engine.get_result(common.sys_info)
        task_id = id_gen()
        task = Task(frame, task_id, serv_type, selected_model)

        if location == common.LOCAL:    # local processing on the edge
            task_queue.put(task)
        elif location == common.OFFLOAD:    # offload to the cloud for processing
            task1 = executor.submit(offload_worker, task)

        # sleep until the duration of INTERVAL seconds has passed
        t_end = time.time()
        if t_end - t_start < INTERVAL:
            dur = INTERVAL - (t_end - t_start)
            time.sleep(dur)




