import torch
import torch.nn as nn
import torch.nn.functional as F

class Model(nn.Module):
    def __init__(self, num_of_image, action_size):
        super(Model, self).__init__()
        #actions = 0 -nothing, 1-jump, 2-crouch, 3-standup
        self.seed = torch.manual_seed(42)

        self.state_size = num_of_image
        self.action_size = action_size

        self.conv1 = nn.Conv2d(num_of_image, 16, kernel_size=3, stride=1, padding=1)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, stride=1, padding=1)
        self.conv3 = nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1)
        self.max_pool = nn.MaxPool2d(kernel_size=2, stride=2)

        self.size = 12800
        self.dropout = nn.Dropout(p=0.2)

        self.fc1 = nn.Linear(self.size, 128)
        self.fc2 = nn.Linear(128, 256)
        self.fc3 = nn.Linear(256, 512)
        self.fc4 = nn.Linear(512, action_size)

    def forward(self, image):
        image = F.relu(self.conv1(image))
        image = self.max_pool(image)

        image = F.relu(self.conv2(image))
        image = self.max_pool(image)

        image = F.relu(self.conv3(image))
        image = self.max_pool(image)

        state = image.view(-1, self.size)
#         state = self.dropout(state)
        state = F.relu(self.fc1(state))
        state = self.dropout(state)

        state = F.relu(self.fc2(state))
        state = self.dropout(state)

        state = F.relu(self.fc3(state))
        state = self.dropout(state)

        action = self.fc4(state)

        return action
