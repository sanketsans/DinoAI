import torch
import torch.nn as nn
import torch.nn.functional as F

class Model(nn.Module):
    def __init__(self, state_size, action_size):
        super(Model, self).__init__()
        #actions = 0 -nothing, 1-jump, 2-crouch, 3-standup
        self.seed = torch.manual_seed(5)

        self.state_size = state_size
        self.action_size = action_size

        self.fc1 = nn.Linear(state_size, 128)
        self.fc2 = nn.Linear(128, 128)
        self.fc3 = nn.Linear(128, action_size)

    def forward(self, state):
        state = F.relu(self.fc1(state))
        state = F.relu(self.fc2(state))

        action = self.fc3(state)

        return action
