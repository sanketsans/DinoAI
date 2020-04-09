import torch
import torch.nn as nn
import torch.nn.functional as F
from model import Model
import random
import numpy as np
import torch.optim as optim
from torch.utils import data
from collections import deque, namedtuple

BUFFER_SIZE = int(1e5)
GAMMA = 1.0
UPDATE_EVERY = 4
BATCH_SIZE = 64
TAU = 1e-3

# device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
device = 'cpu'

class Agent:
    def __init__(self, state_size, action_size):
        self.seed = random.seed(42)
        self.state_size = state_size
        self.action_size = action_size
        self.memory = ReplayBuffer(BUFFER_SIZE, action_size)

        self.t_step = 0
        self.epsilon = 1.0
        self.decay = 0.995
        self.min_eps = 0.005

        self.local_nn = Model(state_size, action_size).to(device)
        self.target_nn = Model(state_size, action_size).to(device)

        self.optimizer = optim.Adam(self.local_nn.parameters(), lr=0.01)

    def step(self, state, action, reward, new_state, done):
        
        self.memory.add(state, action, reward, new_state, done)

        self.t_step = (self.t_step + 1) % UPDATE_EVERY
        if self.t_step == 0:
            if len(self.memory) > BATCH_SIZE:
                experiences = self.memory.sample(BATCH_SIZE)
                self.learn(experiences, GAMMA)

    def act(self, state):
        state = torch.from_numpy(state).float().unsqueeze(0).to(device)

        self.local_nn.eval()
        with torch.no_grad():
            action_values = self.local_nn(state)
        self.local_nn.train()

        self.epsilon = max(self.epsilon*self.decay, self.min_eps)

#         return np.argmax(action_values.cpu().data.numpy())
        if random.random() > self.epsilon:
            return np.argmax(action_values.cpu().data.numpy())
        else:
            return np.random.choice(np.arange(0,3))

    def learn(self, experiences, gamma):
        states, actions, rewards, new_states, dones = experiences
        
        state_itr = iter(states)
        action_itr = iter(actions)
        reward_itr = iter(rewards)
        new_state_itr = iter(new_states)
        done_itr = iter(dones)
                
        for i in range(int(BATCH_SIZE/4)):
            state = np.vstack([next(state_itr), next(state_itr), next(state_itr), next(state_itr)])
            new_state = np.vstack([next(new_state_itr), next(new_state_itr), next(new_state_itr), next(new_state_itr)])
            
            new_state = torch.from_numpy(new_state).float().unsqueeze(0).to(device)
            state = torch.from_numpy(state).float().unsqueeze(0).to(device)
            
            action = next(action_itr)
            reward = next(reward_itr)
            done = next(done_itr)
            
            Q_target_values = self.target_nn(new_state).detach().max(1)[0].unsqueeze(1)
            Q_target = reward + (gamma*Q_target_values*(1-done))

            Q_expected = self.local_nn(state).gather(1, action)

            loss = F.mse_loss(Q_expected, Q_target)
            self.optimizer.zero_grad()

            loss.backward()
            self.optimizer.step()

        self.soft_update(self.local_nn, self.target_nn, TAU)

    def soft_update(self, local_network, target_network, tau):
        for target_params, local_params in zip(target_network.parameters(), local_network.parameters()):
            target_params.data.copy_(tau*local_params.data + (1-tau)*target_params.data)


class ReplayBuffer:
    def __init__(self, buffer_size, action_size):
        self.seed = random.seed(42)
        self.action_size = action_size
        self.memory = deque(maxlen=buffer_size)
        self.experiences = namedtuple("Experiences", field_names=["state","action","reward","new_state","done"])

    def add(self, state, action, reward, new_state, done):
        exp = self.experiences(state, action, reward, new_state, done)
        self.memory.append(exp)

    def sample(self, batch_size):
        experiences = random.sample(self.memory, k=batch_size)

        states = torch.from_numpy(np.vstack([e.state for e in experiences if e is not None])).float().to(device)
        actions = torch.from_numpy(np.vstack([e.action for e in experiences if e is not None])).long().to(device)
        rewards = torch.from_numpy(np.vstack([e.reward for e in experiences if e is not None])).float().to(device)
        new_states = torch.from_numpy(np.vstack([e.new_state for e in experiences if e is not None])).float().to(device)
        dones = torch.from_numpy(np.vstack([e.done for e in experiences if e is not None]).astype(np.uint8)).float().to(device)
        
        states = data.DataLoader(states)
        actions = data.DataLoader(actions)
        rewards = data.DataLoader(rewards)
        new_states = data.DataLoader(new_states)
        dones = data.DataLoader(dones)

        return states, actions, rewards, new_states, dones

    def __len__(self):
        return len(self.memory)