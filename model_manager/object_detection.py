import torch
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


def get_prediction(img, threshold, model, img_id):

    img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    transform = T.Compose([T.ToTensor()])
    img = transform(img)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    img = img.to(device)
    pred = model([img])
    dict = {}
    dict[img_id] = pred
    with open("1080p_info.txt", 'w+') as f:
        f.write(dict)
    if torch.cuda.is_available():
        pred_class = [COCO_INSTANCE_CATEGORY_NAMES[i] for i in list(pred[0]['labels'].cuda().data.cpu().numpy())]
        pred_boxes = [[(i[0], i[1]), (i[2], i[3])] for i in list(pred[0]['boxes'].detach().cpu().numpy())]
        pred_score = list(pred[0]['scores'].detach().cpu().numpy())
    else:
        pred_class = [COCO_INSTANCE_CATEGORY_NAMES[i] for i in list(pred[0]['labels'].numpy())]
        pred_boxes = [[(i[0], i[1]), (i[2], i[3])] for i in list(pred[0]['boxes'].detach().numpy())]
        pred_score = list(pred[0]['scores'].detach().numpy())
    try:
        pred_t = [pred_score.index(x) for x in pred_score if x > threshold][-1]
    except IndexError:
        return None, None
    else:
        pred_boxes = pred_boxes[:pred_t+1]
        pred_class = pred_class[:pred_t+1]
        return pred_boxes, pred_class


def object_detection_api(img_path, img_id, model, rect_th=15, text_th=7, text_size=5, threshold=0.8):

    boxes, pred_cls = get_prediction(img_path, threshold, model, img_id)

    # img = cv2.imread(img_path) # Read image with cv2
    img = cv2.cvtColor(img_path, cv2.COLOR_BGR2RGB)

    if boxes is None and pred_cls is None:
        return img
    for i in range(len(boxes)):
        # Draw Rectangle with the coordinates
        cv2.rectangle(img, boxes[i][0], boxes[i][1], color=(0, 255, 0), thickness=rect_th)
        # Write the prediction class
        cv2.putText(img, pred_cls[i], boxes[i][0], cv2.FONT_HERSHEY_SIMPLEX, text_size, (0, 255, 0), thickness=text_th)
    return img


if __name__ == '__main__':
    # model = generate_model('fasterrcnn_resnet50_fpn')
    # print(model)
    pass
