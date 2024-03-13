from imports import *


''' 
Building a custom gym environment

'''

size = rl_grid_size

# Custom gym environment

class gridScape(Env):
    def __init__(self,grid):
        super(gridScape, self).__init__()

        # Observation and action space 
        # Specifies the total states our DQN has, and the number of actions it can choose from (integer)

        self.observation_space = spaces.Box(low=0, 
                                            high=size,
                                            shape=(size,),
                                           dtype=np.int32)
        self.action_space = spaces.Discrete(size+1)

        # Creating the grid, and a "free cells array" for empty-initialised cells
        self.grid = np.array([grid[i//size][i%size] for i in range(size**2)],dtype=np.int32)

        ptr = 0
        self.free_cells = np.zeros((size**2+1,),dtype=np.int32)
        for i in range(len(self.grid)):
            if self.grid[i] == 0:
                self.free_cells[ptr] = i
                ptr += 1

        # Number of empty-initialised cells
        self.free_length = ptr
        
        # Index of our current position within the free cells array
        self.ind = 0

        # Used for resetting the state
        self.start = grid

    def reset(self):
        self.grid = np.array([self.start[i//size][i%size] for i in range(size**2)])
        self.ind = 0
        return self.grid

    def step(self,action):
        done = False
        
        # Getting position in the grid
        pos = self.free_cells[self.ind]

        # Modifying grid
        old_value = self.grid[pos]
        self.grid[pos] = action

        # If our new grid is valid, reward it. 
        # Otherwise, do not reward, reset grid back to a valid state

        if self.check_valid(pos):
            reward = 1
        else:
            reward = 0
            self.grid[pos] = old_value
            return (self.grid, reward, done, {})


        # If our action is zero (backtracking), reward it a little bit 
        # We want to probe forward as much as possible
        # Also move the pointer back to the previous empty-initialised cell

        if action == 0:
            self.ind = max(self.ind - 1, 0)
            reward = 0.01

        else:
            self.ind += 1

        # If our index is equal to the number of empty-initialised cells, then the grid is complete and valid
        # Return a high reward and tell program we've reached terminal state
        if self.ind == self.free_length:
            reward = 100
            done = True

        return (self.grid, reward, done, {})



    def check_valid(self, pos):

        # Converting our 1d array to virtual 2d
        y = pos//size
        x = pos%size

        # Checking row, column, box
        r, c, b = [0 for _ in range(size+1)], [0 for _ in range(size+1)], [0 for _ in range(size+1)]

        # Mod y, mod x
        my = y%int(size**0.5)
        mx = x%int(size**0.5)

        for i in range(size):

            # Converting i to 2d in terms of location within the box
            di = i//int(size**0.5)
            mi = i%int(size**0.5)

            r[self.grid[size*y+i]] += 1
            c[self.grid[size*i+x]] += 1
            b[self.grid[size*(y-my+di)+x-mx+mi]] += 1
        
        # Initialising at 1 to ignore the number of zeros in an RCB array
        for i in range(1,size):
            if r[i] > 1 or c[i] > 1 or b[i] > 1: return False
        
        return True
            
    def render(self):
        for i in range(size):
            print(self.grid[size*i:size*(i+1)])
