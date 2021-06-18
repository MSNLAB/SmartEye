import sys
import os
import queue
import threading
from concurrent.futures.thread import ThreadPoolExecutor
import edge_globals
import argparse
import time
from local.decision_engine import DecisionEngine
from model_manager.model_cache import load_model
from local.sys_info import SysInfo
from local.video_reader import VideoReader
from loguru import logger
from edge_worker import local_worker, offload_worker, Task, id_gen
from tools.read_config import read_config


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-f', '--file', help="input video file or local camera")
    group.add_argument('-r', '--rtsp', help="RTSP camera", action='store_true')
    parser.add_argument('-s', '--serv', type=int, help="input service demand,"
                                                       "0 for IMAGE_CLASSIFICATION," 
                                                       "1 for OBJECT_DETECTION", required=True)
    parser.add_argument('-i', '--interval', type=int, help="interval between reading two frames in ms", required=True)
    args = parser.parse_args()

    logger.add("log/client_{time}.log", level="INFO")

    file_type = edge_globals.IMAGE_TYPE
    serv_type = args.serv
    INTERVAL = args.interval / 1000.0   # convert into seconds

    input_file = args.file
    if input_file is not None:
        if os.path.isfile(input_file) is False and input_file.isdigit() is False:
            logger.error("input video file or local camera does not exist")
            sys.exit()
        elif input_file.isdigit():
            input_file = int(input_file)

    if input_file is None and args.rtsp is False:
        logger.error("select either video file or RTSP camera")
        sys.exit()

    # load the video analytics models into memory
    edge_globals.loaded_model = load_model()

    # create the objects for video reading, decision making, and information management
    reader = VideoReader(input_file, args.rtsp)
    decision_engine = DecisionEngine(file_type, serv_type)
    edge_globals.sys_info = SysInfo()

    # start the thread pool for processing offloading requests
    WORKER_NUM = read_config("edge-setting", "worker_number")
    executor = ThreadPoolExecutor(max_workers=WORKER_NUM)

    # the queue for local processing task passing
    task_queue = queue.Queue()
    # start the thread for local inference
    local_processor = threading.Thread(target=local_worker, args=(task_queue, ))
    local_processor.start()

    # read frames from video file or camera in loop
    while True:
        frame = reader.read_frame()
        if frame is None:
            logger.error("fail to read a video frame")
            sys.exit()

        t_start = time.time()
        # obtain the CPU and memory usage
        edge_globals.sys_info.update_local_utilization()

        '''
        make decision on video frame processing
        pro_location: local processing or offloading
        pre_proc: how to pre-process the video frame
        selected_model: selected model for inference
        '''
        pro_location, pre_proc, selected_model = decision_engine.get_result(edge_globals.sys_info)

        # create the inference as a task
        task_id = id_gen()
        task = Task(frame, task_id, serv_type, selected_model)

        # local processing on the edge
        if pro_location == edge_globals.LOCAL:
            task_queue.put(task)
        # offload to the cloud for processing
        elif pro_location == edge_globals.OFFLOAD:
            executor.submit(offload_worker, task)

        # sleep until the duration of INTERVAL seconds has passed
        t_end = time.time()
        if t_end - t_start < INTERVAL:
            dur = INTERVAL - (t_end - t_start)
            time.sleep(dur)



