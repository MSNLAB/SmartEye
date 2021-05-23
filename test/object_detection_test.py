import json

from local.offloading import send_frame
from tools.transfer_files_tool import transfer_array_and_str
from local.client_end import Client

if __name__ == '__main__':
    input_file = "../dog.jpg"
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
    # image or video
    store_type = "image"
    client = Client(input_file=input_file, file_type=file_type, service_type=service_type, store_type=store_type)

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
            result_dict = json.loads(result)
            frame_shape = tuple(int(s) for s in result_dict["frame_shape"][1:-1].split(","))
            frame_handled = transfer_array_and_str(result_dict["result"], 'down').reshape(frame_shape)

            # print(frame_handled.shape)
            # cv2.imshow('frame', frame_handled)
            client.local_store.store_image(frame_handled)
