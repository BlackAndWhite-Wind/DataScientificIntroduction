import torch  # PyTorch库
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')  # 设备配置（如有GPU，则使用GPU进行加速）

inputSize = 784  # 输入大小
hiddenSize = 500  # 隐藏层大小
numClasses = 10  # 类
learningRate = 0.001  # alpha学习率
numEpochs = 50  # 训练次数
batchSize = 100  # 连接大小

# MNIST数据集 50k+10k  训练数据集 50000个 测试数据集 10000个
trainDataset = torchvision.datasets.MNIST(root='data', train=True, transform=transforms.ToTensor(), download=True)
testDataset = torchvision.datasets.MNIST(root='data', train=False, transform=transforms.ToTensor())

# 加载MNIST数据集
trainLoader = torch.utils.data.DataLoader(dataset=trainDataset, batch_size=batchSize, shuffle=True)
testLoader = torch.utils.data.DataLoader(dataset=testDataset, batch_size=batchSize, shuffle=False)


# 全连接神经网络模型
class NeuralNetwork(nn.Module):
    def __init__(self, inputSize, hiddenSize, numClasses):
        super(NeuralNetwork, self).__init__()  # 继承
        # 一共设置三层，第一层和第三层用线性回归Linear()函数，中间使用ReLU()函数
        self.fc1 = nn.Linear(inputSize, hiddenSize)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hiddenSize, numClasses)

    # 输入x后输出的output作为下一个的输入，迭代下去，输出output
    def forward(self, x):
        output = self.fc1(x)
        output = self.relu(output)
        output = self.fc2(output)
        return output


model = NeuralNetwork(inputSize, hiddenSize, numClasses).to(device)

criterion = nn.CrossEntropyLoss()  # 定义损失函数
optimizer = torch.optim.Adam(model.parameters(), lr=learningRate)  # 定义优化器

# 进行训练
step = len(trainLoader)  # 训练步长
for epoch in range(numEpochs):
    for i, (images, labels) in enumerate(trainLoader):
        # 移动 tensors 至 GPU 中进行计算
        images = images.reshape(-1, 28 * 28).to(device)
        labels = labels.to(device)

        # 定义前向传递
        outputs = model(images)
        loss = criterion(outputs, labels)

        # 定义反向传播并且优化
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        # 每100步显示一下
        if (i + 1) % 100 == 0:
            print('Epoch [{}/{}], Step [{}/{}], Loss: {:.4f}'
                  .format(epoch + 1, numEpochs, i + 1, step, loss.item()))

# 测试模型
with torch.no_grad():
    correct = 0
    total = 0
    for images, labels in testLoader:
        # 移动 tensors 至 GPU 中进行计算
        images = images.reshape(-1, 28 * 28).to(device)
        labels = labels.to(device)
        outputs = model(images)
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

    print('Accuracy of the network on the 10000 test images: {} %'.format(100 * correct / total))
