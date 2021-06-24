import sys
from config.model_info import edge_object_detection_model
import os
import numpy as np
import queue
import threading
from concurrent.futures import  ThreadPoolExecutor, wait
import edge_globals
import argparse
import time
from local.decision_engine import DecisionEngine
from model_manager.model_cache import load_models
from local.sys_info import SysInfo
from local.video_reader import VideoReader
from loguru import logger
from edge_worker import local_worker, offload_worker, Task, id_gen
from tools.read_config import read_config
from local.local_store import DataStore


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

    # load the video analytics models into memory)
    edge_globals.loaded_model = load_models(edge_object_detection_model)
    # logger.info("edge models have been loaded!")
    # create the objects for video reading, decision making, and information management
    reader = VideoReader(input_file, args.rtsp)
    edge_globals.sys_info = SysInfo()
    decision_engine = DecisionEngine(edge_globals.sys_info)
    edge_globals.datastore = DataStore()
    # start the thread pool for processing offloading requests
    WORKER_NUM = int(read_config("edge-setting", "worker_number"))
    executor = ThreadPoolExecutor(max_workers=WORKER_NUM)

    # the queue for local processing task passing
    task_queue = queue.Queue(int(read_config("edge-setting", "queue_maxsize")))
    # start the thread for local inference
    local_processor = threading.Thread(target=local_worker, args=(task_queue, ))
    local_processor.start()
    
    n = 0
    # read frames from video file or camera in loop
    while True:
        
        frame = reader.read_frame()
        
        n += 1
        if n % 180 != 0:
            continue
        if frame is None:
            wait(edge_globals.thread)
           # print(len(edge_globals.sys_info.offload_delay))
            cloud_average_process_delay = np.average([p.value for p in edge_globals.sys_info.offload_delay])
            logger.info("cloud average process delay:"+str(cloud_average_process_delay))
            logger.info("Service come over!")
            sys.exit()
    
        # obtain the CPU and memory usage
        edge_globals.sys_info.update_local_utilization()

        # create the inference as a task
        task_id = id_gen()
        t_start = time.time()
        task = Task(task_id, frame, serv_type, t_start)

        # obtain the control policy from the configuration file
        edge_policy = read_config("edge-setting", "control_policy")
        # make decision on video frame processing
        task = decision_engine.get_decision(edge_policy, task)
        logger.debug(task.selected_model)
        # local processing on the edge
        if task.location == edge_globals.LOCAL:

            task_queue.put(task, block=True)
           # logger.debug(edge_globals.sys_info.local_delay)
            
        # offload to the cloud for processing
        elif task.location == edge_globals.OFFLOAD:
    
           edge_globals.thread = [executor.submit(offload_worker, task)]
            #if thread.done():
            #   cloud_average_process_delay = np.average([p.value for p in edge_globals.sys_info.offload_delay])
            #   logger.info("cloud average process delay:"+str(cloud_average_process_delay))
        # sleep until the duration of INTERVAL seconds has passed
        t_end = time.time()

        if t_end - t_start < INTERVAL:
            dur = INTERVAL - (t_end - t_start)
            time.sleep(dur)




