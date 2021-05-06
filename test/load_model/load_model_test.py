from torchvision.models import *
from torchvision.models.detection import *
import torch
import os
import cv2
import torchvision
from torchvision import models
from torchvision import transforms
from PIL import Image
import time


classes_file = "D:\PyCharm 2020.3.1\workspace\\video2edge\server\imagenet_classes.txt"
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(
    mean=[0.485, 0.456, 0.406],
    std=[0.229, 0.224, 0.225]

 )])


def load_model(selected_model):
    """
    load the weight file of model
    :param selected_model: model is loaded
    :return: model
    """
    weight_folder = r"D:\PyCharm 2020.3.1\workspace\video2edge\modelweightfile"
    try:
        for file in os.listdir(weight_folder):
            if selected_model in file:
                file_name = file
                break
        assert file_name is not None
    except AssertionError:
        print("there is no matched file!")
    weight_files_path = os.path.join(weight_folder, file_name)
    model = eval(selected_model)()
    model.load_state_dict(torch.load(weight_files_path), False)

    return model

def image_classification(img, selected_model):

    img = Image.open(img)
    # img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    img_t = transform(img)
    batch_t = torch.unsqueeze(img_t, 0)
    model = load_model(selected_model)
    # print(model)
    out = model(batch_t)

    with open(classes_file) as f:
        classes = [line.strip() for line in f.readlines()]

    _, index = torch.max(out, 1)
    percentage = torch.nn.functional.softmax(out, dim=1)[0] * 100
    result = classes[index[0]], percentage[index[0]].item()
    # print(type(result))
    # _, indices = torch.sort(out, descending=True)
    # print([(classes[idx], percentage[idx].item()) for idx in indices[0][:5]])

    return result[0]


if __name__ == '__main__':

    image_path = '../../girl_500.jpg'
    selected_model = 'alexnet'
    t1 = time.time()
    result = image_classification(image_path, selected_model)
    t2 = time.time()
    print(t2 - t1)
    print(result)
