# DinoAI
RL trained agent to play t-rex game

I created the game using pygame. The window size is 600, 150. The dino is placed at 40 units from the left. Each object(dino, cactus and birds) has its own width. Considering this, I calculated the position at which dino will collide with the object(s). 

### Approach I


I created a value based observation state space. The state space consists of :
- I convereted the entire distance(width) of the screen into discrete space of 100 bins.
- Distance of the obstacle from the dino and allocated them into their own bins. 
- The ground speed.
- The gap between 1st and 2nd obstacle. 
- The heigth of the obstacle. 

So, I have 5 state objects and 3 actions ( 0 - nothing to do, 1 - jump, 2- crouch, it might vary for two agent scripts). 

I used DQN algorithm to train the model with 2 hidden layers, 1 input layer and 1 output layer(nodes might vary for two model scripts). I trained them for 5 hrs on a CPU and the results were still average. 

[![Results]](https://www.youtube.com/watch?v=mrzyq8SkX0A)


### Approach II 

I tried to use pixel data instead of value based approach. For this, I used gym_chrome_dino ( https://pypi.org/project/gym-chrome-dino/) gym based environment. I provide a stack of 4 continous image data with pre-processed (80x160) frames. So each input is (4x80x160). I then used the same amount of fully connected layers to train the network. 
I take ages to train the same on a CPU. So, I did not complete the training. 

If you have a GPU it'd be great if you could train the network.

