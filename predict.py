import torch
import os
import argparse
import numpy as np
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
from models.mcnet_binary_7_23 import MCNET
from torch.autograd import Variable
import matplotlib.font_manager as fm

parser = argparse.ArgumentParser()
parser.add_argument('--infer_path', type = str, default = 'work/infer_mask01.jpg', help = 'predict image')
parser.add_argument('--infer_dir_path', type = str, default = 'work/infer_dir', help = 'predict image dir')
parser.add_argument('--result_path', type = str, default = 'work/result/', help = 'save image dir')
parser.add_argument('--test_weights', type = str, default = 'ckp-7-23/model_1_0.6096.pth', help = 'test weights')
parser.add_argument('--gpus', type = str, default = '0', help = 'which gpu, gpu ids: e.g. 0  0,1,2, 0,2. use -1 for CPU')

opt = parser.parse_args()
print(opt)

label_dic = {
    "0": "NoMaskImage",
    "1": "MaskImage",
}

os.environ['CUDA_VISIBLE_DEVICES'] = opt.gpus
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

transform_predict = transforms.Compose([
    transforms.Resize((7, 7)),
    transforms.ToTensor(),
])

# image = Image.open(opt.infer_path)
# image = transform_predict(image).unsqueeze(0).to(device)
model = MCNET()
model.load_state_dict(torch.load(opt.test_weights))
model.cuda()

def image_add_text(img_path, text, left, top, text_color=(255, 0, 0), text_size=13):
    img = Image.open(img_path)
    draw = ImageDraw.Draw(img)
    fontStyle = ImageFont.truetype(fm.findfont(fm.FontProperties(family='DejaVu Sans')), text_size, encoding="utf-8")
    draw.text((left, top), text, text_color, font=fontStyle)
    return img

with torch.no_grad():
    model.eval()

    file_list = os.listdir(opt.infer_dir_path)
    for file in file_list:
        cur_path = os.path.join(opt.infer_dir_path, file)

        image = Image.open(cur_path)
        image = transform_predict(image).unsqueeze(0).to(device)
        image = Variable(image.cuda())

        image = image * 255 -128
        image = image / 256

        out = model(image)
        label = np.argmax(out.cpu().numpy())
        print('Image is {}'.format(label_dic[str(label)]))  
        im = image_add_text(cur_path, label_dic[str(label)], 20, 10, text_color=(0, 0, 255), text_size=30)
        im.save(opt.result_path + 'pre_' +  str(file) + '.jpg')
 
print("Ending!")