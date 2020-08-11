# BNN
Binary Neural Network in Pytorch

## 内容
基于BNN实现口罩判定二分类器并生成硬件仿真网表
具体可见项目报告书（包括数据集来源，网络结构，生成测试网表的过程）

BNN论文已经上传，优化　https://github.com/itayhubara/BinaryNet.pytorch
对第一层也进行低比特量化
修正sign() 在权重和激活值错误二值化结果
常数pad
实现剪枝，方法同ann_pq中的剪枝方法