from __future__ import print_function
import argparse
import os
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms
from torch.autograd import Variable
from models.binarized_modules import  BinarizeLinear,BinarizeConv2d
from models.binarized_modules import  Binarize,HingeLoss
from MyData import MyData
from torchsummary import summary
import numpy as np 

from models.mcnet_binary_7_32 import MCNET

# python main_mask_7_32.py
# Training settings
parser = argparse.ArgumentParser(description='PyTorch MNIST Example')
parser.add_argument('--batch_size', type=int, default=16, metavar='N',
                    help='input batch size for training (default: 256)')
parser.add_argument('--test_batch_size', type=int, default=1, metavar='N',
                    help='input batch size for testing (default: 1000)')
parser.add_argument('--epochs', type=int, default=200, metavar='N',
                    help='number of epochs to train (default: 10)')
parser.add_argument('--lr', type=float, default=0.001, metavar='LR',
                    help='learning rate (default: 0.001)')
parser.add_argument('--momentum', type=float, default=0.5, metavar='M',
                    help='SGD momentum (default: 0.5)')
parser.add_argument('--no-cuda', action='store_true', default=False,
                    help='disables CUDA training')
parser.add_argument('--seed', type=int, default=1, metavar='S',
                    help='random seed (default: 1)')
parser.add_argument('--gpus', default=0,
                    help='gpus used for training - e.g 0,1,3')
parser.add_argument('--log_interval', type=int, default=10, metavar='N',
                    help='how many batches to wait before logging training status')
parser.add_argument('--train_path', type = str, default = 'data/train.txt', 
                    help = '.txt path of train')
parser.add_argument('--test_path', type = str, default = 'data/eval.txt', 
                    help = '.txt path of train')
parser.add_argument('--num_workers', type = int, default = 8, 
                    help = 'num of workers')
# parser.add_argument('--pre_weights', type = str, default = 'ckp-v1.pad1/model_37_0.8849.pth',
#                     help = 'pre weights')

args = parser.parse_args()
args.cuda = not args.no_cuda and torch.cuda.is_available()

torch.manual_seed(args.seed)
if args.cuda:
    torch.cuda.manual_seed(args.seed)

kwargs = {'num_workers': 1, 'pin_memory': True} if args.cuda else {}

transform_train = transforms.Compose([
    transforms.Resize((7,7)),
    transforms.RandomCrop((7,7)),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),

])
transform_val=transforms.Compose([ 
	transforms.Resize((7,7)),
	transforms.ToTensor(),
])

trainset = MyData(args.train_path, transform = transform_train)
valset = MyData(args.test_path, transform = transform_val)
train_loader=torch.utils.data.DataLoader(trainset, batch_size=args.batch_size, 
                                        shuffle=True, num_workers=args.num_workers)
test_loader=torch.utils.data.DataLoader(valset, batch_size=args.test_batch_size, 
                                        shuffle=False, num_workers=args.num_workers)

model = MCNET()
# if args.pre_weights:
#     model.load_state_dict(torch.load(args.pre_weights))
#     for name, param in model.named_parameters():
#                 print(name, '\n', param.size(), '\n')

if args.cuda:
    # torch.cuda.set_device(3)
    torch.cuda.set_device(0)
    model.cuda()

summary(model, (3, 7, 7))

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=args.lr)

MODEL_PATH = "ckp-7-32/" 
if not os.path.exists(MODEL_PATH):
    os.makedirs(MODEL_PATH)	

def train(epoch):
    model.train()
    for batch_idx, (data, target) in enumerate(train_loader):
        if args.cuda:
            data, target = data.cuda(), target.cuda()
        data, target = Variable(data), Variable(target)

        data = data * 255 -128
        data = data / 256

        optimizer.zero_grad()
        output = model(data)
        loss = criterion(output, target)

        if epoch%40==0:
            optimizer.param_groups[0]['lr']=optimizer.param_groups[0]['lr']*0.1
            
        optimizer.zero_grad()
        loss.backward()
        for p in list(model.parameters()):
            if hasattr(p,'org'): 
                p.data.copy_(p.org)   
        optimizer.step()
        for p in list(model.parameters()):
            if hasattr(p,'org'):
                p.org.copy_(p.data.clamp_(-1,1))

        if batch_idx % args.log_interval == 0:
            print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
                epoch, batch_idx * len(data), len(train_loader.dataset),
                100. * batch_idx / len(train_loader), loss.item()))

max_result = []
def test(epoch):
    model.eval()
    test_loss = 0
    total=0
    correct = 0
    with torch.no_grad():
        for data, target in test_loader:
            if args.cuda:
                data, target = data.cuda(), target.cuda()
            data, target = Variable(data), Variable(target)

            data = data * 255 -128
            data = data / 256

            output = model(data)
            test_loss += criterion(output, target).item() # sum up batch loss
            pred = output.data.max(1, keepdim=True)[1] # get the index of the max log-probability
            correct += pred.eq(target.data.view_as(pred)).cpu().sum()
            total+=data.size(0)

    result = (1.0*correct.numpy())/total
    result = round(result, 4)
    test_loss /= len(test_loader.dataset)
    print('\nTest set: Epoch_{} Average loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n'.format(
        epoch, test_loss, correct, len(test_loader.dataset),
        100. * correct / len(test_loader.dataset)))
    
    max_result.append(result)
    if result == max(max_result):
        max_result[epoch - 1] = result
        torch.save(model.state_dict(), MODEL_PATH + 'model_' + str(epoch) + '_' + str(result) + '.pth')

for epoch in range(1, args.epochs + 1):
    train(epoch)
    test(epoch)
    if epoch%40==0:
        optimizer.param_groups[0]['lr']=optimizer.param_groups[0]['lr']*0.1
