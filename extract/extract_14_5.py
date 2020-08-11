import torch
import torch.nn as nn
import torchvision.transforms as transforms
import os
from torch.autograd import Variable
import argparse
import numpy as np 
from PIL import Image
import csv
import shutil

import sys
sys.path.append('../')
from models.mcnet_binary_14_5 import MCNET

# python extract_14_5.py 
parser = argparse.ArgumentParser()
parser.add_argument('--gpu', type=str, default='0', help='gpu ids: e.g. 0  0,1,2, 0,2. use -1 for CPU')
parser.add_argument('--image', type=str, default='../infer_mask01.jpg', help='which an image will be detected')

parser.add_argument('--test_weights', type = str, default = '../ckp/ckp-14-5/model_3_0.8663.pth', help = 'test weights')
parser.add_argument('--fm_save_path', type = str, default = 'extract_out/fm_14_5/', help = 'test weights')
parser.add_argument('--param_save_path', type = str, default = 'extract_out/param_14_5/', help = 'test weights')
opt = parser.parse_args()
print(str(opt) + '\n')

os.environ["CUDA_VISIBLE_DEVICES"] = opt.gpu

label_dic = {
    "0": "NoMaskImage",
    "1": "MaskImage",
}

transform_test = transforms.Compose([
    transforms.Resize((14, 14)),
    transforms.ToTensor(),
])
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

FM_ROOT_PATH = opt.fm_save_path
if not os.path.exists(FM_ROOT_PATH):
    os.makedirs(FM_ROOT_PATH)
else:
    shutil.rmtree(FM_ROOT_PATH)
    os.makedirs(FM_ROOT_PATH)

PARAM_ROOT_PATH = opt.param_save_path
if not os.path.exists(PARAM_ROOT_PATH):
    os.makedirs(PARAM_ROOT_PATH)
else:
    shutil.rmtree(PARAM_ROOT_PATH)
    os.makedirs(PARAM_ROOT_PATH)

#  extract feature map
model = MCNET()
model.load_state_dict(torch.load(opt.test_weights))
model.cuda()
model.eval()


for name, param in model.named_parameters():
    # print(name, '\n', param.size(), '\n', param.cpu())
    param_numpy = param.cpu().detach().numpy()
    zero_numpy = np.argwhere(param_numpy == 0)

    if len(zero_numpy) == 0:
        print(str(name) + ' no zero!\n')
        param_numpy.tofile(PARAM_ROOT_PATH + str(name) + '.param.bin')
        np.save(PARAM_ROOT_PATH + str(name), param_numpy)
    else:
        print(str(name) + 'have zero!\n')

image = Image.open(opt.image)  # RGB
image = transform_test(image).unsqueeze(0).to(device) 
image = Variable(image.cuda()) 
image = image * 255 -128
image = image / 256

def hook(module, input, output):
    print(output.size(1))
    input_tensor = input[0]
    print(input_tensor.size())
    input_numpy = input_tensor.cpu().data.numpy()
    output_numpy = output.cpu().data.numpy()   
    zero_numpy = np.argwhere(input_numpy == 0)

    if len(zero_numpy) == 0:
        print('No zero in input')

        # if input_tensor.size(1) == 3:
        #     np.save(FM_ROOT_PATH + 'input.fm', input_numpy)
        #     input_numpy.tofile(FM_ROOT_PATH + 'input.fm.bin')
        #     print('save input fm\n')

        if input_tensor.size(1) == 3:
        # if input_tensor.size(1) == 3 and output.size(1) == 3:
            np.save(FM_ROOT_PATH + 'feature1.fm', input_numpy)
            input_numpy.tofile(FM_ROOT_PATH + 'feature1.fm.bin')
            print('save feature1 fm\n')

        if input_tensor.size(1) == 5:
        # if input_tensor.size(1) == 3 and output.size(1) == 16:
            np.save(FM_ROOT_PATH + 'feature2.fm', input_numpy)
            input_numpy.tofile(FM_ROOT_PATH + 'feature2.fm.bin')
            print('save feature2 fm\n') 

        if input_tensor.size(1) == 16:
            np.save(FM_ROOT_PATH + 'feature3.fm', input_numpy)
            input_numpy.tofile(FM_ROOT_PATH + 'feature3.fm.bin')
            print('save feature3 fm\n')

        if input_tensor.size(1) == 32:
            np.save(FM_ROOT_PATH + 'feature4.fm', input_numpy)
            input_numpy.tofile(FM_ROOT_PATH + 'feature4.fm.bin')
            print('save feature4 fm\n')

        if output.size(1) == 2:
            np.save(FM_ROOT_PATH + 'out.fm', output_numpy)
            output_numpy.tofile(FM_ROOT_PATH + 'out.fm.bin')
            print('save out fm\n')
    else:
        print('Zero in input\n')

a = []
for name, module in model._modules.items():
    handle = module.register_forward_hook(hook)
    a.append(handle)

out = model(image)
print(out)
label = np.argmax(out.cpu().detach().numpy())
print('Image is {}'.format(label_dic[str(label)]) + '\n')

for i in a:
    i.remove()


