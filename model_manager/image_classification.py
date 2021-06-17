import os
import cv2
from torchvision.models import *
import torch
from torchvision import transforms
from PIL import Image
from loguru import logger


def preprocess(img):
    """Preprocess image which will be preprocessed

    :param img: image
    :return: preprocessed image
    """
    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])
    # img = Image.open(img)
    img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    img_t = transform(img)
    batch_t = torch.unsqueeze(img_t, 0)
    return batch_t


def load_model(selected_model):
    """Load the weight file of selected model.

    :param selected_model: The name of the model to load
    :return: model: loaded model
    """

    weight_folder = os.path.join(os.path.dirname(__file__), "../cv_model")
    try:
        for file in os.listdir(weight_folder):
            if selected_model in file:
                file_name = file
                break
        assert file_name is not None
    except AssertionError:
        print("there is no matched file!")
    weight_files_path = os.path.join(weight_folder, file_name)
    model = eval(selected_model)(pretrained=False)
    model.load_state_dict(torch.load(weight_files_path))
    model.eval()
    return model


def image_classification(img, model):
    """Image prediction.

    Predict the class of image and return the result.

    :param img: image frame
    :param model: loaded model
    :return: predict result.
    """
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    batch_t = preprocess(img)
    batch_t_gpu = batch_t.to(device)
    out = model(batch_t_gpu)
    classes_file = os.path.join(os.path.dirname(__file__), "imagenet_classes.txt")

    with open(classes_file) as f:
        classes = [line.strip() for line in f.readlines()]

    _, index = torch.max(out, 1)
    percentage = torch.nn.functional.softmax(out, dim=1)[0] * 100
    result = classes[index[0]], percentage[index[0]].item()
    return result[0]


if __name__ == '__main__':

    image_path = '../info_store/handled_result/dog.jpg'
    selected_model = 'resnet101'
    result = image_classification(image_path, selected_model)
    # print(dir(models))
    print(result)
