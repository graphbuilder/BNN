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

from models.mcnet_binary import MCNET

parser = argparse.ArgumentParser()
parser.add_argument('--gpu', type=str, default='0', help='gpu ids: e.g. 0  0,1,2, 0,2. use -1 for CPU')
parser.add_argument('--image', type=str, default='infer_mask01.jpg', help='which an image will be detected')
parser.add_argument('--test_weights', type = str, default = 'ckp-v1.pad1/model_37_0.8849.pth', help = 'test weights')
opt = parser.parse_args()
print(str(opt) + '\n')

os.environ["CUDA_VISIBLE_DEVICES"] = opt.gpu

label_dic = {
    "0": "NoMaskImage",
    "1": "MaskImage",
}

transform_test = transforms.Compose([
    transforms.Resize((28, 28)),
    transforms.ToTensor(),
])
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

FM_ROOT_PATH = "/home/aiden00/abwu_workspace/BinaryNet.pytorch/fm/"   
if not os.path.exists(FM_ROOT_PATH):
    os.makedirs(FM_ROOT_PATH)
else:
    shutil.rmtree(FM_ROOT_PATH)
    os.makedirs(FM_ROOT_PATH)

PARAM_ROOT_PATH = "/home/aiden00/abwu_workspace/BinaryNet.pytorch/param/"   
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

def set_dir(filepath, file):
    if not os.path.exists(filepath):
        os.mkdir(filepath)
    # else:
    #     shutil.rmtree(filepath)
    #     os.mkdir(filepath)
    PATH = str(filepath) + '/' + str(file)
    with open(PATH, 'w') as f: 
        f.seek(0)
        f.truncate()
    return PATH

for name, param in model.named_parameters():
    # print(name, '\n', param.size(), '\n', param.cpu())
    param_numpy = param.cpu().detach().numpy()
    zero_numpy = np.argwhere(param_numpy == 0)

    filename = set_dir(PARAM_ROOT_PATH, str(name) + '.txt')  # .split('.')[0]

    if len(zero_numpy) == 0:
        print(str(name) + ' no zero!\n')
        param_numpy.tofile(PARAM_ROOT_PATH + str(name) + '.param.bin')
        np.save(PARAM_ROOT_PATH + str(name), param_numpy)

        output_param_c = param_numpy.shape[0]
        input_param_c = param_numpy.shape[1]
        param_h = param_numpy.shape[2]
        param_w = param_numpy.shape[3]

        with open(filename, 'a') as f:
            for i in range(output_param_c):
                for j in range(input_param_c):
                    for k in range(param_h):
                        for l in range(param_w):      
                            f.write(str(int(param_numpy[i, j, k, l])) + ",")
                    f.write('\n')
                f.write('\n') 
        f.close()   

    else:
        print(str(name) + 'have zero!\n')

image = Image.open(opt.image)  # RGB
image = transform_test(image).unsqueeze(0).to(device) 
image = Variable(image.cuda()) 
image = image * 255 -128
image = image / 256

def hook(module, input, output):
    input_tensor = input[0]
    print(input_tensor.size())
    input_numpy = input_tensor.cpu().data.numpy()
    output_numpy = output.cpu().data.numpy()   
    zero_numpy = np.argwhere(input_numpy == 0)

    if len(zero_numpy) == 0:
        print('No zero in input')

        if input_tensor.size(1) == 3:
            np.save(FM_ROOT_PATH + 'input.fm', input_numpy)
            input_numpy.tofile(FM_ROOT_PATH + 'input.fm.bin')
            print(input_numpy)
            print('save input fm\n')

            input_numpy = input_numpy.squeeze()
            filename = set_dir(FM_ROOT_PATH, 'input.txt')
            fm_c = input_numpy.shape[0]
            fm_h = input_numpy.shape[1]
            fm_w = input_numpy.shape[2]

            with open(filename, 'a') as f:
                for i in range(fm_c):
                    for j in range(fm_h):
                        for k in range(fm_w):    
                            f.write(str(int(input_numpy[i, j, k])) + ",")
                        f.write('\n')
                    f.write('\n')
            f.close()   

        if input_tensor.size(1) == 4:
            np.save(FM_ROOT_PATH + 'feature1.fm', input_numpy)
            input_numpy.tofile(FM_ROOT_PATH + 'feature1.fm.bin')
            print('save feature1 fm\n')

            input_numpy = input_numpy.squeeze()
            filename = set_dir(FM_ROOT_PATH, 'feature1.txt')
            fm_c = input_numpy.shape[0]
            fm_h = input_numpy.shape[1]
            fm_w = input_numpy.shape[2]

            with open(filename, 'a') as f:
                for i in range(fm_c):
                    for j in range(fm_h):
                        for k in range(fm_w):    
                            f.write(str(int(input_numpy[i, j, k])) + ",")
                        f.write('\n')
                    f.write('\n')
            f.close() 

        if input_tensor.size(1) == 8:
            np.save(FM_ROOT_PATH + 'feature2.fm', input_numpy)
            input_numpy.tofile(FM_ROOT_PATH + 'feature2.fm.bin')
            print('save feature2 fm\n') 

            input_numpy = input_numpy.squeeze()
            filename = set_dir(FM_ROOT_PATH, 'feature2.txt')
            fm_c = input_numpy.shape[0]
            fm_h = input_numpy.shape[1]
            fm_w = input_numpy.shape[2]

            with open(filename, 'a') as f:
                for i in range(fm_c):
                    for j in range(fm_h):
                        for k in range(fm_w):    
                            f.write(str(int(input_numpy[i, j, k])) + ",")
                        f.write('\n')
                    f.write('\n')
            f.close() 

        if input_tensor.size(1) == 16:
            np.save(FM_ROOT_PATH + 'feature3.fm', input_numpy)
            input_numpy.tofile(FM_ROOT_PATH + 'feature3.fm.bin')
            print('save feature3 fm\n')

            input_numpy = input_numpy.squeeze()
            filename = set_dir(FM_ROOT_PATH, 'feature3.txt')
            fm_c = input_numpy.shape[0]
            fm_h = input_numpy.shape[1]
            fm_w = input_numpy.shape[2]

            with open(filename, 'a') as f:
                for i in range(fm_c):
                    for j in range(fm_h):
                        for k in range(fm_w):    
                            f.write(str(int(input_numpy[i, j, k])) + ",")
                        f.write('\n')
                    f.write('\n')
            f.close() 

        if input_tensor.size(1) == 32:
            np.save(FM_ROOT_PATH + 'feature4.fm', input_numpy)
            input_numpy.tofile(FM_ROOT_PATH + 'feature4.fm.bin')
            print('save feature4 fm\n')

            input_numpy = input_numpy.squeeze()
            filename = set_dir(FM_ROOT_PATH, 'feature4.txt')
            fm_c = input_numpy.shape[0]
            fm_h = input_numpy.shape[1]
            fm_w = input_numpy.shape[2]

            with open(filename, 'a') as f:
                for i in range(fm_c):
                    for j in range(fm_h):
                        for k in range(fm_w):    
                            f.write(str(int(input_numpy[i, j, k])) + ",")
                        f.write('\n')
                    f.write('\n')
            f.close() 

        if output.size(1) == 2:
            print(output.size())
            np.save(FM_ROOT_PATH + 'out.fm', output_numpy)
            output_numpy.tofile(FM_ROOT_PATH + 'out.fm.bin')
            print('save out fm\n')

            output_numpy = output_numpy.squeeze()
            filename = set_dir(FM_ROOT_PATH, 'out.txt')
            fm_c = output_numpy.shape[0]

            with open(filename, 'a') as f:
                for i in range(fm_c):
                    f.write(str(int(output_numpy[i])) + ",")
                    f.write('\n')
            f.close() 

    else:
        print('Zero in input\n')

a = []
for name, module in model._modules.items():
    handle = module.register_forward_hook(hook)
    a.append(handle)

out = model(image)
label = np.argmax(out.cpu().detach().numpy())
print('Image is {}'.format(label_dic[str(label)]) + '\n')

for i in a:
    i.remove()


