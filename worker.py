import common
import sys
import time
import string
import random
from loguru import logger
from tools.read_config import read_config
from tools.transfer_files_tool import transfer_array_and_str
from frontend_server.offloading import send_frame
from local.preprocessor import PreProcessor
from local.local_processor import LocalProcessor

image_url = read_config("transfer-url", "image_url")


def id_gen(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class Task:
    def __init__(self, frame, task_id, serv_type, model):
        self.frame = frame
        self.task_id = task_id
        self.serv_type = serv_type
        self.selected_model = model


def local_worker(task_queue):
    local_processor = LocalProcessor()
    while True:
        task = task_queue.get()
        t_start = time.time()
        result = local_processor.process(task.frame, task.model, loaded_model)
        t_end = time.time()
        processing_delay = t_end - t_start
        if task.serv_type == common.IMAGE_CLASSIFICATION:
            sys_info.append_local_delay(t_start, processing_delay)
        elif task.serv_type == common.OBJECT_DETECTION:
            sys_info.append_offload_delay(t_start, processing_delay)

def offload_worker(task):
    preprocessor = PreProcessor()

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