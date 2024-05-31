import torch
import torchvision.transforms as transforms 
import torch.nn as nn 
from torch.nn import Conv2d
from torch.nn import Linear
from torch.nn import MaxPool2d
from torch.nn import ReLU
from torch.nn import LogSoftmax
import numpy as np
import os
import random
from torch.utils.data import Dataset, DataLoader
from PIL import Image


# hyperparameters
batch_size = 64
learning_rate = 0.001
split_rate = 0.8
epochs = 10


classes = ('0','1','2','3','4','5','6','7','8','9')


training_images = []
training_labels = []

test_images = []
test_labels = []

# Getting images

for root, dir, files in os.walk('digits/'):
    for file in files:
        image_class = root[-1]
        image_path = os.path.join(root, file)

        r = random.random()
        if r < split_rate:
            training_images.append(image_path)
            training_labels.append(image_class)
        else:
            test_images.append(image_path)
            test_labels.append(image_class)


# Designing custom dataset

class DigitDataset(Dataset):

    def __init__(self, images, labels, transform=None):
        self.images = images

        image_transform = transforms.Compose([transforms.ToTensor(), transforms.Grayscale(num_output_channels=1)])

        for i, img in enumerate(self.images):

            image = Image.open(img)

            image_tensor = image_transform(image)
            self.images[i] = image_tensor

        self.labels = labels
        self.transform = transform

    def __getitem__(self, index):

        image = self.images[index]
        label = np.int64(self.labels[index])

        return image, label
    
    def __len__(self):
        return len(self.images)



train_dataset = DigitDataset(training_images, training_labels)
test_dataset = DigitDataset(test_images, test_labels)

train_dataloader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
test_dataloader = DataLoader(test_dataset, batch_size=batch_size, shuffle=True)





# Model

class DigitNetwork(nn.Module):
    def __init__(self):
        super(DigitNetwork, self).__init__()

        # Initial convolutional layer and ReLU loss
        # Note torch convolutions are dynamic. Image sizes are 64x64
        self.conv1 = Conv2d(in_channels=1, out_channels=20,
            kernel_size=(5, 5))
        self.relu1 = ReLU()

        # Initial pool layer
        self.maxpool1 = MaxPool2d(kernel_size=(2, 2), stride=(2, 2))

        # After flattening the image, connect to regular NN

        # Fully connected layer
        self.fc1 = Linear(in_features=20*30*30, out_features=500)
        self.relu3 = ReLU()

        # Softmax classifier
        self.classifier = Linear(in_features=500, out_features=len(classes))
        self.logSoftmax = LogSoftmax(dim=1)

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
    
device = "cuda" if torch.cuda.is_available() else "cpu"

model = DigitNetwork().to(device)
print(model)


# Loss function for multi-class classification
loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

def train(dataloader, model, loss_fn, optimizer):
    size = len(dataloader.dataset)
    model.train()


    for batch, (image, label) in enumerate(dataloader):

        image = image.to(device)
        label = label.to(device)

        # Compute prediction error
        pred = model(image)
        loss = loss_fn(pred, label)

        # Backpropagation
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()

        if batch % 100 == 0:
            loss, current = loss.item(), (batch + 1) * len(image)
            print(f"loss: {loss:>7f}  [{current:>5d}/{size:>5d}]")


def test(dataloader, model, loss_fn):
    """ Test the model on the given dataloader.
    Args:
        dataloader (DataLoader): Dataloader for the test data
        model (nn.Module): Trained model
        loss_fn (nn.Module): Loss function for evaluation           """
    
    # Initialize variables
    size = len(dataloader.dataset)
    num_batches = len(dataloader)
    model.eval()
    test_loss, correct = 0, 0
    
    # Disable gradient computation
    with torch.no_grad():
        # Iterate over the test data
        for X, y in dataloader:
            # Move data to device
            X, y = X.to(device), y.to(device)
            
            # Forward pass
            pred = model(X)
            
            # Compute the loss
            test_loss += loss_fn(pred, y).item()
            
            # Compute the number of correct predictions
            correct += (pred.argmax(1) == y).type(torch.float).sum().item()
        
    # Compute the average loss
    test_loss /= num_batches
    
    # Compute the accuracy
    correct /= size
    
    # Print the test results
    print(f"Test Error: \n Accuracy: {(100*correct):>0.1f}%, Avg loss: {test_loss:>8f} \n")


for t in range(epochs):
    print(f"Epoch {t+1}\n-------------------------------")
    train(train_dataloader, model, loss_fn, optimizer)
    test(test_dataloader, model, loss_fn)
print("Done!")

# Saving model
torch.save(model.state_dict(), "server/digit_model.pt")