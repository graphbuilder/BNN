import torch.nn as nn
import torch
from torchsummary import summary
from .binarized_modules import  BinarizeConv2d

class MCNET(nn.Module):
    def __init__(self):
        super(MCNET, self).__init__()
        # self.features = nn.Sequential(
        #     BinarizeConv2d(3, int(4*self.ratioInfl), kernel_size=3, padding=1, bias=False),  # 28
        #     nn.MaxPool2d(kernel_size=2, stride=2),  # 14
        #     nn.Hardtanh(inplace=True),

        #     BinarizeConv2d(int(4*self.ratioInfl), int(8*self.ratioInfl), kernel_size=3, padding=1,bias=False),  # 14
        #     nn.MaxPool2d(kernel_size=2, stride=2),  # 7
        #     nn.Hardtanh(inplace=True),

        #     BinarizeConv2d(int(8*self.ratioInfl), int(16*self.ratioInfl), kernel_size=3, padding=0, bias=False),  # 5
        #     nn.Hardtanh(inplace=True),

        #     BinarizeConv2d(int(16*self.ratioInfl), int(32*self.ratioInfl), kernel_size=3, padding=0, bias=False),  # 3
        #     nn.Hardtanh(inplace=True),

        #     BinarizeConv2d(int(32*self.ratioInfl), int(2*self.ratioInfl), kernel_size=3, padding=0, bias=False),  # 3->1

        # )

        self.p0 = nn.Sequential(
            nn.ConstantPad2d(1, value=1),
        )

        self.features0 = nn.Sequential(
            BinarizeConv2d(3, 4, kernel_size=3, padding=0, bias=False),  # 28
            nn.Hardtanh(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),  # 14
        )
        
        self.features1 = nn.Sequential(
            nn.ConstantPad2d(1, value=1),
            BinarizeConv2d(4, 8, kernel_size=3, padding=0, bias=False),  # 14
            nn.Hardtanh(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),  # 7
        )

        self.features2 = nn.Sequential(
            BinarizeConv2d(8, 16, kernel_size=3, padding=0, bias=False),  # 5
            nn.Hardtanh(inplace=True),
        )

        self.features3 = nn.Sequential(
            BinarizeConv2d(16, 32, kernel_size=3, padding=0, bias=False),  # 3
            nn.Hardtanh(inplace=True),
        )

        self.features4 = nn.Sequential(
            BinarizeConv2d(32, 2, kernel_size=3, padding=0, bias=False),  # 3->1
            nn.Hardtanh(inplace=True),
        )

    def forward(self, inputs):
        x = self.p0(inputs)       
        x = self.features0(x)
        x = self.features1(x)
        x = self.features2(x)
        x = self.features3(x)
        x = self.features4(x)
        x = x.view(x.size(0), -1)
        return x

if __name__ == "__main__":
    img = torch.rand((1, 3, 28, 28), dtype = torch.float)
    net = MCNET()
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = net.to(device)
    summary(model, (3, 28, 28))
    