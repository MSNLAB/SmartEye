import cv2
import torchvision
from torchvision.models import *
from torchvision import models
import torch
from torchvision import transforms
from PIL import Image


classes_file = "D:\PyCharm 2020.3.1\workspace\\video2edge\server\imagenet_classes.txt"
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(
    mean=[0.485, 0.456, 0.406],
    std=[0.229, 0.224, 0.225]

 )])


# def generate_model(selected_model):
#
#     model = eval(selected_model)(pretrained=True)
#     model.eval()
#
#     return model


def image_classification(img, model):

    # img = Image.open(image_path)
    img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    img_t = transform(img)
    batch_t = torch.unsqueeze(img_t, 0)
    # model = generate_model(selected_model)
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

    # image_path = 'girl.jpg'
    # selected_model = 'alexnet'
    # result = image_classification(image_path, selected_model)
    print(dir(models))
