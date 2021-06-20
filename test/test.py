import os
import time
import torch
import torchvision
from PIL import Image
from torchvision import transforms as T
import cv2
from torchvision.models.detection import *
from loguru import logger


COCO_INSTANCE_CATEGORY_NAMES = [
    '__background__', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
    'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'N/A', 'stop sign',
    'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
    'elephant', 'bear', 'zebra', 'giraffe', 'N/A', 'backpack', 'umbrella', 'N/A', 'N/A',
    'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
    'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket',
    'bottle', 'N/A', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl',
    'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
    'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'N/A', 'dining table',
    'N/A', 'N/A', 'toilet', 'N/A', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
    'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'N/A', 'book',
    'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'
]

n = 0

def load_model(selected_model):

    weight_folder = os.path.join(os.path.dirname(__file__), "cv_model")
    try:
        for file in os.listdir(weight_folder):
            if selected_model in file:
                file_name = file
                break
        assert file_name is not None
    except AssertionError as err:

        logger.exception("there is no matched file!")
    else:

        weight_files_path = os.path.join(weight_folder, file_name)
        file_load = torch.load(weight_files_path)
        model = eval(selected_model)()
        model.load_state_dict(file_load, False)
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model.eval()
        model.to(device)
        return model


def get_prediction(img_path, model, threshold):

    img = Image.fromarray(cv2.cvtColor(img_path, cv2.COLOR_BGR2RGB))
   #img = Image.open(img_path)
    transform = T.Compose([T.ToTensor()])
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    #logger.debug(device)
    img = transform(img)
    img = img.to(device)
    pred = model([img])
   # if device == "cuda":
    pred_class = [COCO_INSTANCE_CATEGORY_NAMES[i] for i in list(pred[0]['labels'].cuda().data.cpu().numpy())]
    pred_boxes = [[(i[0], i[1]), (i[2], i[3])] for i in list(pred[0]['boxes'].detach().cpu().numpy())]
    pred_score = list(pred[0]['scores'].detach().cpu().numpy())
    #else:
   # pred_class = [COCO_INSTANCE_CATEGORY_NAMES[i] for i in list(pred[0]['labels'].numpy())]
   # pred_boxes = [[(i[0], i[1]), (i[2], i[3])] for i in list(pred[0]['boxes'].detach().numpy())]
   # pred_score = list(pred[0]['scores'].detach().numpy())
    try:
        pred_t = [pred_score.index(x) for x in pred_score if x > threshold][-1]
    except IndexError:
        return None, None
    else:
        pred_boxes = pred_boxes[:pred_t + 1]
        pred_class = pred_class[:pred_t + 1]
        return pred_boxes, pred_class



def object_detection_api(img_path, model, threshold=0.5, rect_th=3, text_size=3, text_th=3):
    t6 = time.time()
    boxes, pred_cls = get_prediction(img_path, model, threshold)
    t7 = time.time()
    logger.debug("get coordinate:"+str(t7-t6))
    
    # Get predictions
   # img = cv2.imread(img_path)
    # Read image with cv2
    img = cv2.cvtColor(img_path, cv2.COLOR_BGR2RGB)
    if boxes is None and pred_cls is None:
        return img
    # Convert to RGB
    #t4 = time.time()
    global n
    for i in range(len(boxes)):
        # Draw Rectangle with the coordinates
        cv2.rectangle(img, boxes[i][0], boxes[i][1], color=(0, 255, 0), thickness=rect_th)
        # Write the prediction class
        cv2.putText(img, pred_cls[i], boxes[i][0], cv2.FONT_HERSHEY_SIMPLEX, text_size, (0, 255, 0),
                    thickness=text_th)
        cv2.imwrite("./result/result"+str(n)  +".jpg", img)
    #t5 = time.time()
   # logger.debug("draw time:"+str(t5-t4))
    n += 1
    return img


def reader(cap):

    if cap.isOpened():
        ret, frame = cap.read()
        if ret:
            return frame
        else:
            cap.release()
            return None



if __name__ == "__main__":


    selected_model = 'maskrcnn_resnet50_fpn'
    #"fasterrcnn_mobilenet_v3_large_320_fpn"
    #"fasterrcnn_resnet50_fpn"
    # "maskrcnn_resnet50_fpn"
    
    #"retinanet_resnet50_fpn"
    #"fasterrcnn_mobilenet_v3_large_fpn"
  
    video = "VIRAT_S_000006.mp4"
#    video = "people.jpg"
    cap = cv2.VideoCapture(video)
    
    t1 = time.time()
    model =  load_model(selected_model)
    t2 = time.time()
    frame_number = 0
    total_prediction_time = 0
    while True:

        frame = reader(cap)
       # logger.debug(frame)
        if frame is None:
            break

        frame_number += 1
    
        if frame_number == 100:
            break
    # "maskrcnn_resnet50_fpn"
        t3 = time.time()
        object_detection_api(frame, model, threshold=0.8)
        t4 = time.time()
        prediction_time = t4 - t3 
        logger.debug("prediction time:"+str(t4-t3))
        total_prediction_time +=  prediction_time
    #logger.debug("load model time:"+str(t2-t1))
    #/logger.debug("prediction:"+str(t3-t2))
    logger.info(selected_model)
    logger.debug("load model time:"+str(t2-t1))
    logger.debug("average prediction time:"+str(total_prediction_time/frame_number))
