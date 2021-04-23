from client.offloading import send_frame
from client.local_store import LocalStore
from tools.transfer_files_tool import transfer_array_and_str
from transmission.client_end import Client


if __name__ == '__main__':
    input_file = "../85652500-1-192.mp4"
    # input_file = 0
    # while True:
    #     try:
    #         file_type = input("please input file type: image or video\n")
    #         assert file_type is not None
    #         assert file_type == "image" or file_type == "video"
    #         service_type = input("please input file type: image classification or object detection\n")
    #         assert service_type is not None
    #         assert service_type == "image classification" or service_type == "object detection"
    #     except AssertionError:
    #         print("please input again:")
    #     else:
    #         break
    file_type = "image"
    service_type = "object detection"

    client = Client(input_file=input_file, file_type=file_type, service_type=service_type)

    while True:
        # get frames
        frame = client.reader.read_file()
        # preprocessing frames
        if frame is None:
            print("service comes over!")
            exit()
        frame = client.preprocessing.pre_process_image(frame, **client.msg_dict)
        # transmission
        result = send_frame(client.picture_url, frame, client.selected_model)
        if service_type == "image classification":
            print(result)
        else:
            frame_handled = transfer_array_and_str(result, 'down')
            client.local_store.store_image(frame_handled)
