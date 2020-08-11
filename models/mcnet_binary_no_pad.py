'''
no pad, 7 conv layers, Acc:68.12%, 
failed

'''
import torch.nn as nn
import torch
from torchsummary import summary
from .binarized_modules import  BinarizeConv2d

class MCNET(nn.Module):
    def __init__(self):
        super(MCNET, self).__init__()

        self.features0 = nn.Sequential(
            BinarizeConv2d(3, 4, kernel_size=3, padding=0, bias=False),  # 28->26
            nn.Hardtanh(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),  # 26->13
        )

        self.features1 = nn.Sequential(
            BinarizeConv2d(4, 8, kernel_size=3, padding=0, bias=False),  # 13->11
            nn.Hardtanh(inplace=True),
            # nn.MaxPool2d(kernel_size=2, stride=2),  # 7
        )

        self.features2 = nn.Sequential(
            BinarizeConv2d(8, 16, kernel_size=3, padding=0, bias=False),  # 11->9
            nn.Hardtanh(inplace=True),
        )

        self.features3 = nn.Sequential(
            BinarizeConv2d(16, 32, kernel_size=3, padding=0, bias=False),  # 9->7
            nn.Hardtanh(inplace=True),
        )


        self.features4 = nn.Sequential(
            BinarizeConv2d(32, 64, kernel_size=3, padding=0, bias=False),  # 7->5
            nn.Hardtanh(inplace=True),
        )

        self.features5 = nn.Sequential(
            BinarizeConv2d(64, 32, kernel_size=3, padding=0, bias=False),  # 5->3
            nn.Hardtanh(inplace=True),
        )

        self.features6 = nn.Sequential(
            BinarizeConv2d(32, 2, kernel_size=3, padding=0, bias=False),  # 3->1
            nn.Hardtanh(inplace=True),
        )


    def forward(self, inputs):     
        x = self.features0(inputs)
        x = self.features1(x)
        x = self.features2(x)
        x = self.features3(x)
        x = self.features4(x)
        x = self.features5(x)
        x = self.features6(x)
        x = x.view(x.size(0), -1)

        return x

    