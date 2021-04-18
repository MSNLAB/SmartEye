import json
# import mmap
from client.offloading import send_frame
from client.preprocessing import PreProcessing
from tools import make_request
from client.decision_engine import DecisionEngine
from tools.network_condition import get_network_condition
from tools.transfer_files_tool import save_file, transfer_file_to_str
from client.video_reader import VideoReader


if __name__ == '__main__':

    input_file = "/home/wxz/Desktop/20200827153531.mp4"
    initial_url = "http://127.0.0.1:5000/initial"
    picture_url = "http://127.0.0.1:5000/pictures_handler"
    video_file_url = "http://127.0.0.1:5000/video_file_handler"
    # initial_url = "http://39.99.145.157:5000/initial"
    # picture_url = "http://39.99.145.157:5000/pictures_handler"
    # video_file_url = "http://39.99.145.157:5000/video_file_handler"
    requirement_type = ('image', 'image classification')
    reader = VideoReader()
    service_delay, net_speed = get_network_condition(initial_url)
    print(service_delay)
    print(net_speed)
    decision_engine = DecisionEngine(
        service_delay=service_delay, requirement_type=requirement_type, net_condition=net_speed
    )
    preprocessing = PreProcessing()

    msg_dict, selected_model = decision_engine.get_decision_result()
    print(selected_model)
    while True:
        # get frames
        frame = reader.read_file(input_file)
        print("read_file")
        print(frame)
        # preprocessing frames
        frame = preprocessing.pre_process_image(frame, **msg_dict)
        print("processed image")
        print(frame)
        # transmission
        result = send_frame(picture_url, frame, selected_model)
        print(result)







