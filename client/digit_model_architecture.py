from torch import nn

# Model

class DigitNetwork(nn.Module):
    def __init__(self):
        super(DigitNetwork, self).__init__()

        # Initial convolutional layer and ReLU loss
        # Note torch convolutions are dynamic. Image sizes are 64x64
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=20,
            kernel_size=(5, 5))
        self.relu1 = nn.ReLU()

        # Initial pool layer
        self.maxpool1 = nn.MaxPool2d(kernel_size=(2, 2), stride=(2, 2))

        # After flattening the image, connect to regular NN

        # Fully connected layer
        self.fc1 = nn.Linear(in_features=20*30*30, out_features=500)
        self.relu3 = nn.ReLU()

        # Softmax classifier
        self.classifier = nn.Linear(in_features=500, out_features=10)
        self.logSoftmax = nn.LogSoftmax(dim=1)

    def forward(self, x):

        # Apply convolution and max pool
        x = self.conv1(x)
        x = self.relu1(x)
        x = self.maxpool1(x)

        # Flatten
        x = x.view(x.size(0), -1)

        # Deep layer
        x = self.fc1(x)
        x = self.relu3(x)

        # pass the output to our softmax classifier to get output prediction
        x = self.classifier(x)
        output = self.logSoftmax(x)

        # return the output predictions
        return output