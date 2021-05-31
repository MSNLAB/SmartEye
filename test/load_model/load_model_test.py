from tools.read_config import read_config
import torch
import os
from torchvision import transforms
from PIL import Image
import time
from server.msg_transfer_service import load_model_files_advance


transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])


def load_model(selected_model):
    """
    load the weight file of model
    :param selected_model: model is loaded
    :return: model
    """

    preload_models = read_config("preload-models")
    # print(preload_models)
    if selected_model in preload_models:
        # print(1)
        model = eval(selected_model)()
        model.load_state_dict(result_dict[selected_model], False)
        model.eval()
    # print(model)
    else:
        weight_folder = read_config("models-path", "path")
        try:
            for file in os.listdir(weight_folder):
                if selected_model in file:
                    file_name = file
                    break
            assert file_name is not None
        except AssertionError:
            print("there is no matched file!")
        # print(selected_model)
        weight_files_path = os.path.join(weight_folder, file_name)
        model = eval(selected_model)()
        model.load_state_dict(torch.load(weight_files_path), False)
        model.eval()

    return model
# def load_model(selected_model):
#     """
#     load the weight file of model
#     :param selected_model: model is loaded
#     :return: model
#     """
#     weight_folder = read_config.read_config("models-path", "path")
#     try:
#         for file in os.listdir(weight_folder):
#             if selected_model in file:
#                 file_name = file
#                 break
#         assert file_name is not None
#     except AssertionError:
#         print("there is no matched file!")
#     weight_files_path = os.path.join(weight_folder, file_name)
#     model = eval(selected_model)(pretrained=False)
#     model.load_state_dict(torch.load(weight_files_path), False)
#     model.eval()
#     return model


def image_classification(img, selected_model):

    img = Image.open(img)
    # img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    img_t = transform(img)
    batch_t = torch.unsqueeze(img_t, 0)
    model = load_model(selected_model)
    with torch.no_grad():
        out = model(batch_t)

    classes_file = read_config("classes-file", "classes_file")
    with open(classes_file) as f:
        classes = [line.strip() for line in f.readlines()]
    _, index = torch.max(out, 1)
    percentage = torch.nn.functional.softmax(out, dim=1)[0] * 100
    result = classes[index[0]], percentage[index[0]].item()

    return result[0]


if __name__ == '__main__':

    # alexnet mnasnet0_5 mnasnet1_0 mobilenet_v2 resnet101 shufflenet_v2_x0_5 squeezenet1_0 vgg11 wide_resnet101_2
    # "googlenet inception_v3"
    # densenet121, densenet161
    result_dict = load_model_files_advance()
    # print(result_dict.keys())
    image_path = '../../info_store/handled_result/dog.jpg'
    selected_model = 'mnasnet0_5'
    # print(result_dict[selected_model])
    t1 = time.time()
    result = image_classification(image_path, selected_model)
    t2 = time.time()
    print(t2 - t1)
    print(result)
