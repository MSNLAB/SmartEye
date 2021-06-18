import sys
import time
import string
import random
import edge_globals
from loguru import logger
from tools.read_config import read_config
from tools.transfer_files_tool import transfer_array_and_str
from frontend_server.offloading import send_frame
from local.preprocessor import PreProcessor
from local.local_processor import LocalProcessor
from edge_globals import sys_info
from edge_globals import loaded_model

# the video frame handler of the forwarding server
frame_handler = read_config("flask-url", "video_frame_url")


# generate the id for a task
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
        preprocessor = PreProcessor(task.frame)
        frame = preprocessor.preprocess(**task.msg_dict)
        result = local_processor.process(task.frame, task.model, loaded_model)
        t_end = time.time()
        processing_delay = t_end - t_start
        if task.serv_type == edge_globals.IMAGE_CLASSIFICATION:
            sys_info.append_local_delay(t_start, processing_delay)
        elif task.serv_type == edge_globals.OBJECT_DETECTION:
            sys_info.append_offload_delay(t_start, processing_delay)


def offload_worker(task):
    preprocessor = PreProcessor()

    frame = preprocessor.preprocess_image(task.frame, **task.msg_dict)
    file_size = sys.getsizeof(frame)
    # send the video frame to the server
    try:
        result_dict, start_time, processing_delay, arrive_transfer_server_time = \
            send_frame(frame_handler, frame, selected_model)
    except Exception as err:
        logger.exception("return back err!")
    else:
        bandwidth = file_size / arrive_transfer_server_time
        if task.serv_type == edge_globals.IMAGE_CLASSIFICATION:
            result = result_dict["prediction"]
            sys_info.append(start_time, processing_delay, bandwidth)
            logger.info("offload:"+result)
        elif task.serv_type == edge_globals.OBJECT_DETECTION:
            frame_shape = tuple(int(s) for s in result_dict["frame_shape"][1:-1].split(","))
            frame_handled = transfer_array_and_str(result_dict["result"], 'down').reshape(frame_shape)
            sys_info.append(start_time, processing_delay, bandwidth)
            logger.info("offload object detection works well!")