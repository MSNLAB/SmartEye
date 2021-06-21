import sys
import time
import string
import random
import edge_globals
from loguru import logger
from tools.read_config import read_config
from tools.transfer_files_tool import transfer_array_and_str
from frontend_server.offloading import send_frame
from local.preprocessor import preprocess
from model_manager import object_detection, image_classification

# the video frame handler of the forwarding server
frame_handler = read_config("flask-url", "video_frame_url")


# generate the id for a task
def id_gen(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class Task:
    def __init__(self, task_id, frame, serv_type):
        self.task_id = task_id
        self.frame = frame
        self.serv_type = serv_type
        self.selected_model = None
        self.location = None
        self.new_size = None
        self.new_qp = None


def local_inference(task):
    """local inference for a video frame"""
    

    model = edge_globals.loaded_model[task.selected_model]
    if task.serv_type == edge_globals.OBJECT_DETECTION:
        result = object_detection.object_detection_api(task.frame, model, threshold=0.8)
        return result
    if task.serv_type == edge_globals.IMAGE_CLASSIFICATION:
        result = image_classification.image_classification(task.frame, model)
        return result


def local_worker(task_queue):
    
    while True:
         
        # get a task from the queue
        task = task_queue.get(block=True)
    
        t_start = time.time()
        # locally process the task
        result = local_inference(task)
        t_end = time.time()
        processing_delay = t_end - t_start
    
        # record the processing delay
        edge_globals.sys_info.append_local_delay(t_start, processing_delay)

        if task.serv_type == edge_globals.IMAGE_CLASSIFICATION:
            logger.info("image classification result:"+result)
        elif task.serv_type == edge_globals.OBJECT_DETECTION:
            logger.info("object detection works well! please go to info_store/handled_result to check.")
            edge_globals.datastore.store_image(result)


def offload_worker(task):
    task = preprocess(task)
    file_size = sys.getsizeof(task.frame)
    t_start = time.time()
    # send the video frame to the server
    try:
        result_dict, start_time, processing_delay, arrive_transfer_server_time = \
            send_frame(frame_handler, task.frame, task.selected_model)
    except Exception as err:
        logger.exception("offloading error")
    else:
        # record the bandwidth and the processing delay
        bandwidth = file_size / arrive_transfer_server_time
        edge_globals.sys_info.append_bandwidth(t_start, bandwidth)
        edge_globals.sys_info.append_offload_delay(t_start, processing_delay)

        if task.serv_type == edge_globals.IMAGE_CLASSIFICATION:
            result = result_dict["prediction"]
            logger.info("offload:"+result)
        elif task.serv_type == edge_globals.OBJECT_DETECTION:
            frame_shape = tuple(int(s) for s in result_dict["frame_shape"][1:-1].split(","))
            frame_handled = transfer_array_and_str(result_dict["result"], 'down').reshape(frame_shape)
