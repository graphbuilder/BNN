import torch.nn as nn
import torch
from torchsummary import summary

class DummyModule(nn.Module):
    def __init__(self):
        super(DummyModule, self).__init__()

    def forward(self, x):
        # print("Dummy, Dummy.")
        return x

class MCNET(nn.Module):
    def __init__(self):
        super(MCNET, self).__init__()

        # self.features = nn.Sequential(
        #     nn.Conv2d(3, 4, kernel_size=3, padding=1),  # 224
        #     nn.BatchNorm2d(4, affine=True),
        #     # DummyModule(),
        #     nn.ReLU(inplace=True),
        #     nn.MaxPool2d(kernel_size=2, stride=2),  # 112

        #     nn.Conv2d(4, 8, kernel_size=3, padding=1),  # 112
        #     nn.BatchNorm2d(8, affine=True),
        #     # DummyModule(),
        #     nn.ReLU(inplace=True),
        #     nn.MaxPool2d(kernel_size=2, stride=2),  # 56

        #     nn.Conv2d(8, 16, kernel_size=3, padding=1),  # 56
        #     nn.BatchNorm2d(16, affine=True),
        #     # DummyModule(),
        #     nn.ReLU(inplace=True),
        #     nn.MaxPool2d(kernel_size=2, stride=2),  # 28

        #     nn.Conv2d(16, 32, kernel_size=3, padding=1),  # 28
        #     nn.BatchNorm2d(32, affine=True),
        #     # DummyModule(),
        #     nn.ReLU(inplace=True),
        #     nn.MaxPool2d(kernel_size=2, stride=2),  # 14

        #     nn.Conv2d(32, 64, kernel_size=3, padding=1),  # 14 
        #     nn.BatchNorm2d(64, affine=True), 
        #     # DummyModule(),
        #     nn.ReLU(inplace=True),
        #     nn.MaxPool2d(kernel_size=2, stride=2),  # 7 

        #     nn.Conv2d(64, 32, kernel_size=3, padding=0),  # 5
        #     nn.BatchNorm2d(32, affine=True),
        #     # DummyModule(),
        #     nn.ReLU(inplace=True),

        #     nn.Conv2d(32, 16, kernel_size=3, padding=0),  # 3
        #     nn.BatchNorm2d(16, affine=True),
        #     # DummyModule(),
        #     nn.ReLU(inplace=True),

        #     nn.Conv2d(16, 2, kernel_size=3, padding=0),  # 3->1
        # )

        # self.features = nn.Sequential(
        #     nn.Conv2d(3, 4, kernel_size=3, padding=1),  # 56
        #     nn.BatchNorm2d(4, affine=True),
        #     # DummyModule(),
        #     nn.ReLU(inplace=True),
        #     nn.MaxPool2d(kernel_size=2, stride=2),  # 28

        #     nn.Conv2d(4, 8, kernel_size=3, padding=1),  # 28
        #     nn.BatchNorm2d(8, affine=True),
        #     # DummyModule(),
        #     nn.ReLU(inplace=True),
        #     nn.MaxPool2d(kernel_size=2, stride=2),  # 14

        #     nn.Conv2d(8, 16, kernel_size=3, padding=1),  # 14
        #     nn.BatchNorm2d(16, affine=True),
        #     # DummyModule(),
        #     nn.ReLU(inplace=True),
        #     nn.MaxPool2d(kernel_size=2, stride=2),  # 7

        #     nn.Conv2d(16, 32, kernel_size=3, padding=0),  # 5
        #     nn.BatchNorm2d(32, affine=True),
        #     # DummyModule(),
        #     nn.ReLU(inplace=True),

        #     nn.Conv2d(32, 64, kernel_size=3, padding=0),  # 3 
        #     nn.BatchNorm2d(64, affine=True), 
        #     # DummyModule(),
        #     nn.ReLU(inplace=True),

        #     nn.Conv2d(64, 2, kernel_size=3, padding=0),  # 3->1

        # )

        self.features = nn.Sequential(
            nn.Conv2d(3, 4, kernel_size=3, padding=1),  # 28
            nn.BatchNorm2d(4, affine=True),
            # DummyModule(),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),  # 14

            nn.Conv2d(4, 8, kernel_size=3, padding=1),  # 14
            nn.BatchNorm2d(8, affine=True),
            # DummyModule(),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),  # 7

            nn.Conv2d(8, 16, kernel_size=3, padding=0),  # 5
            nn.BatchNorm2d(16, affine=True),
            # DummyModule(),
            nn.ReLU(inplace=True),

            nn.Conv2d(16, 32, kernel_size=3, padding=0),  # 3
            nn.BatchNorm2d(32, affine=True),
            # DummyModule(),
            nn.ReLU(inplace=True),

            nn.Conv2d(32, 2, kernel_size=3, padding=0),  # 3->1

        )

        # self.classifier = nn.Sequential(
        #     nn.Linear(6272, num_classes),
        # )

    def forward(self, inputs):
        x = self.features(inputs)
        x = x.view(x.size(0), -1)
        # x = self.classifier(x)

        return x

if __name__ == "__main__":
    img = torch.rand((1, 3, 28, 28), dtype = torch.float)
    net = MCNET()
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = net.to(device)
    summary(model, (3, 28, 28))
    