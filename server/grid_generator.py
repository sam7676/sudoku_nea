import random
from itertools import product


unique_coordinates = ((0,0), (1,3), (2,6), (3,1), (4,4), (5,7), (6,2), (7,5), (8,8))
rcbs = []
for y, x in unique_coordinates:
    row = [(y,i) for i in range(9)]
    col = [(i,x) for i in range(9)]

    top_left_y = 3 * (y//3)
    top_left_x = 3 * (x//3)
    box = [(top_left_y, top_left_x + i) for i in range(3)] + [(top_left_y+1, top_left_x + i) for i in range(3)] + [(top_left_y+2, top_left_x + i) for i in range(3)]

    rcbs.append(row)
    rcbs.append(col)
    rcbs.append(box)

def transfer_grid(nums, input_dims, output_dims):

    if input_dims == 1:
        #preprocessing
        nums=nums.replace(' ','')
        if len(nums)!=81: 
            raise Exception
    
    if input_dims == 1 and output_dims == 1:
        grid = nums

    if input_dims == 1 and output_dims == 2:

        grid = [[0 for i in range(9)] for j in range(9)]
        for i, digit in enumerate(nums):
            y = i//9
            x = i%9
            grid[y][x] = int(digit)

    elif input_dims == 1 and output_dims == 3:

        grid = [[0 for i in range(9)] for j in range(9)]
        for i, digit in enumerate(nums):
            y = i//9
            x = i%9
            if int(digit) != 0:
                grid[y][x] = [int(digit)]
            else:
                grid[y][x] = [1,2,3,4,5,6,7,8,9]


    elif input_dims == 2 and output_dims == 1:

        grid = ''
        for y in nums:
            for x in y:
                grid += str(x)
    
    elif input_dims == 2 and output_dims == 2:
        grid = [[0 for i in range(9)] for j in range(9)]
        for y in range(9):
            for x in range(9):
                grid[y][x] = nums[y][x]

    elif input_dims == 2 and output_dims == 3:
        
        grid = [[0 for i in range(9)] for j in range(9)]

        for y in range(9):
            for x in range(9):
                if nums[y][x] == 0:
                    grid[y][x] = [1,2,3,4,5,6,7,8,9]
                else:
                    grid[y][x] = [nums[y][x]]

    elif input_dims == 3 and output_dims == 1:

        grid = ''
        for y in nums:
            for x in y:
                grid += str(x[0])

    elif input_dims == 3 and output_dims == 2:

        grid = [[0 for i in range(9)] for j in range(9)]
        for y in range(9):
            for x in range(9):
                if len(nums[y][x])==1:
                    grid[y][x] = nums[y][x][0]
                else:
                    grid[y][x] = 0

    elif input_dims == 3 and output_dims == 3:
        grid = [[0 for i in range(9)] for j in range(9)]
        for y in range(9):
            for x in range(9):
                grid[y][x] = nums[y][x][:]
        
    return grid

def print_grid(grid, dims):
    #Prints grid to terminal. Processes differently whether string or list

    if dims == 2:
        grid = transfer_grid(grid, 2, 1)
        dims = 1

    if dims == 1:
        stri='| '
        for i in range(len(grid)):
            if i%27==0:
                print('+','-'*5,'+','-'*5,'+','-'*5,'+',sep="")

            if grid[i]=='0':
                stri+=' '
            else:                
                stri+=grid[i]
            if i%3==2:
                stri+=' | '
            if i%9==8:
                print(stri)
                stri='| '
        print('+','-'*5,'+','-'*5,'+','-'*5,'+',sep="")

    elif dims == 3:
        print(f"+---+{'-'*31}+{'-'*31}+{'-'*31}+")
        print('|   | 0         1         2         | 3         4         5         | 6         7         8         |')
        print(f"+---+{'-'*31}+{'-'*31}+{'-'*31}+")
        for i in range(len(grid)):

            col_string = f'| {i} | '
            for j in range(len(grid[i])):

                stri=''
                for k in grid[i][j]:
                    stri+=str(k)
                stri+=' '*(9-len(stri))

                col_string+=stri
                col_string+=' '
                if j%3==2:
                    col_string+='| '
            print(col_string)
            if i%3==2:
                print(f"+---+{'-'*31}+{'-'*31}+{'-'*31}+")
    
def store_grid(grid):
    #Makes and returns a new copy of the grid without modifying the original
    temp=[]
    if type(grid[0][0])==list:
        for i in range(len(grid)):
            temp2 = []
            for j in range(len(grid[i])):
                temp2.append(grid[i][j][:])
            temp.append(temp2[:])
    else:
        for i in range(len(grid)):
            temp2 = []
            for j in range(len(grid[i])):
                temp2.append(grid[i][j])
            temp.append(temp2[:])
    return temp

class constraint:
    def __init__(self, nums):

        # Input: any dim
        # Output: 1 dim
        
        if type(nums) == str:
            grid = transfer_grid(nums, 1, 3)
        elif type(nums[0][0])==int:
            grid = transfer_grid(nums, 2, 3)
        else:
            grid = nums

        self.next_move = []

        self.ans, self.layer, self.moves = self.start(grid, 0, 0)
        self.ans = transfer_grid(self.ans, 3, 1)

        if self.next_move[0] == "Bowman":
            # Update answer
            y,x = self.next_move[1][0]
            self.next_move[-1] = [[self.ans[9*y+x]]]

    def return_cords(self,grid):
        #Returns co-ordinates of the cell with the minimal notes in it. Used for bowman
        for a in range(2,10):
            for i in range(9):
                for j in range(9):
                    if len(grid[i][j])==a:
                        return [i,j,a]
    
    def start(self, grid, layer, moves):

        #Runs a process of executing all the non-guessing commands. 
        #Calculates whether a change has taken place based off the number of moves.

        old_moves = -1
        while old_moves != moves:
            old_moves = moves
            grid, moves = self.one_note_instance(grid, moves)
            grid, moves = self.remove_notes(grid, moves)
            if old_moves==moves:
                grid, moves = self.partner(grid, moves)

            
        if self.check_complete(grid):
            return grid, layer, moves
        
        if self.check_valid(grid):
            y1,x1, num = self.return_cords(grid)

            if not self.next_move:
                self.next_move = ["Bowman", [(y1,x1)], [grid[y1][x1]], -1]


            for n in range(num):
                g = store_grid(grid)

                g[y1][x1]=[g[y1][x1][n]]

                #If it is not the final answer, but still works, we do this step again recursively
                ans = self.start(g,layer+1, moves+1) 
                if ans!=None:
                    return ans   

    def check_complete(self,grid):
        #checks grid to see if its complete - length of all cells = 1.
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if len(grid[i][j])!=1:
                    return False
        return True
    
    def check_valid(self,grid):
        # Checks the validity of the grid and 
        # whether there are any cells that are empty and therefore invalid
        for i in range(len(grid)):
            for j in range(len(grid)):
                if grid[i][j] == []:
                    return False
        return True
    
    def remove_notes(self, grid, moves):
        
        for array in rcbs:

            if not self.next_move:
                old_array = [grid[y][x] for y,x in array]


            move = False
    
            for i, z in enumerate(array):
                yi, xi = z

                if len(grid[yi][xi]) == 1:

                    val = grid[yi][xi][0]

                    for j, w in enumerate(array):
                        yj, xj = w

                        if i!=j and val in grid[yj][xj]:
                            grid[yj][xj].remove(val)

                            move = True

            if move:
                
                if not self.next_move:
                    self.next_move = ["Remove", array, old_array, [grid[y][x] for y,x in array]]

                moves += 1

        return grid, moves

    def one_note_instance(self, grid, moves):

        for array in rcbs:

            if not self.next_move:
                old_array = [grid[y][x] for y,x in array]

            s = [set(grid[y][x]) for y,x in array]

            move = False

            for note in range(1, 10):

                note_count = 0

                for i, z in enumerate(array):
                    y, x = z

                    if note in s[i]:
                        note_count += 1

                if note_count == 1:

                    for i, z in enumerate(array):
                        y, x = z

                        if note in s[i] and len(grid[y][x]) > 1:
                            grid[y][x] = [note]

                            move = True                

            if move:
                if not self.next_move:
                    self.next_move = ["One note", array, old_array, [grid[y][x] for y,x in array]]
                moves += 1

        return grid, moves
    
    def partner(self,grid, moves):

        for array in rcbs:

            if not self.next_move:
                old_array = [grid[y][x] for y,x in array]

            move = False
            for val in range(1,10):

                
                nums = [grid[y][x] for y,x in array]

                
                #minimum, minimum potential nums, indexes of minimum potentials
                max_length = 10
                minimum_potential = []
                minimum_indices = []

                def run(potential, used, max_length, minimum_potential, minimum_indices):
                    
                    #if the potential length is minimal - if len(group 1)=5, then len(group 2..)<4
                    if len(potential) < max_length and len(potential) < 5:

                        for i in potential: #each member of potential list
                            for j in range(len(nums)): #original list

                                #if the potential number in loop is in one of the nums terms + index isn't used
                                if i in nums[j] and j not in used:

                                    #store the potential and used list
                                    potential_store = potential[:]
                                    used_store = used[:]

                                    #any new numbers that the cell matches the potential number and haven't been used
                                    for k in nums[j]:
                                        if k not in potential_store:
                                            potential_store.append(k)

                                    #add the list position to used indexes
                                    used_store.append(j)

                                    #if new potential has same length as used list (closed loop, no more to explore)
                                    if len(potential_store)==len(used_store):

                                        #if the length of potential is less than the minimum, assign minimals
                                        if len(potential_store) < max_length: 
                                            max_length = len(potential_store)
                                            minimum_potential = potential_store
                                            minimum_indices = used_store

                                        # Otherwise, no need to minimise
                                            
                                    else:

                                        #keep exploring potential until it cuts off at 0 
                                        return run(potential_store,used_store,max_length,minimum_potential,minimum_indices)
                    
                    #returns the smallest findable groups and their indexes
                    return [minimum_potential,minimum_indices]

                #runs the recursive loop
                minimum_potential, minimum_indices = run([val],
                                                 [], 
                                                 max_length, 
                                                 minimum_potential,
                                                 minimum_indices)



                for i, z in enumerate(array):
                    y,x = z
                    if i in minimum_indices:
                        for j in grid[y][x]:
                            if j not in minimum_potential:
                                grid[y][x].remove(j)
                                move = True
                
                
            if move:
                if not self.next_move:
                    self.next_move = ["Partner", array, old_array, [grid[y][x] for y,x in array]]
                moves += 1
        
        return grid, moves

class algorithm_x:
    def __init__(self,nums):

        # This originates from another Sudoku solver, not made by me.
        # Its benefit over my developed algorithm (above) is that it is much faster 
        # due to it being a backtrack solver and independent of solution difficulty.
        # However, I have stripped this algorithm of its solving inputs/outputs, 
        # and it is now used to calculate the number of solutions a grid has.

        # Original code:         https://www.cs.mcgill.ca/~aassaf9/python/sudoku.txt


        if type(nums) == str:
            grid = transfer_grid(nums, 1, 2)
        else:
            grid = transfer_grid(nums, 2, 2)

        
        self.ans = self.solving(grid)

        # Input: any dim
        # Output: int


    def solving(self,grid): #grid, solution
        self.sols=0
        X = ([("rc", rc) for rc in product(range(9), range(9))] +
            [("rn", rn) for rn in product(range(9), range(1, 9 + 1))] +
            [("cn", cn) for cn in product(range(9), range(1, 9 + 1))] +
            [("bn", bn) for bn in product(range(9), range(1, 9 + 1))])
        Y = dict()
        for r, c, n in product(range(9), range(9), range(1, 9 + 1)):
            b = (r // 3) * 3 + (c // 3) # Box number
            Y[(r, c, n)] = [
                ("rc", (r, c)),
                ("rn", (r, n)),
                ("cn", (c, n)),
                ("bn", (b, n))]
        X, Y = self.exact_cover(X, Y)
        for i, row in enumerate(grid):
            for j, n in enumerate(row):
                if n:
                    self.select(X, Y, (i, j, n))
        for i in self.solve(X,Y,[]):
            pass
    def exact_cover(self,X, Y):
        X = {j: set() for j in X}
        for i, row in Y.items():
            for j in row:
                X[j].add(i)
        return X, Y
    def solve(self,X, Y, solution):
        if not X:
            if self.sols<2:
                self.sols+=1
                yield
        else:
            c = min(X, key=lambda c: len(X[c]))
            for r in list(X[c]):
                solution.append(r)
                cols = self.select(X, Y, r)
                for s in self.solve(X, Y, solution):
                    yield
                self.deselect(X, Y, r, cols)
                solution.pop()
                if self.sols>=2:
                    break
    def select(self,X, Y, r):
        cols = []
        for j in Y[r]:
            for i in X[j]:
                for k in Y[i]:
                    if k != j:
                        X[k].remove(i)
            cols.append(X.pop(j))
        return cols
    def deselect(self,X, Y, r, cols):
        for j in reversed(Y[r]):
            X[j] = cols.pop()
            for i in X[j]:
                for k in Y[i]:
                    if k != j:
                        X[k].add(i)

class generate(algorithm_x):
    def __init__(self,attempts=[0,1],grid_inp='000000000000000000000000000000000000000000000000000000000000000000000000000000000'):

        # Input: 1 dim
        # Output: 1 dim

        final_grid = self.generate_complete(grid_inp)
        hardest_generate = []

        for i in range(attempts[1]):
            grid, changes = self.remove_complete(store_grid(final_grid), attempts[0], grid_inp)

            grid_information = constraint(grid)

            layer = grid_information.layer
            moves = grid_information.moves

            difficulty = (layer + 1) * moves * changes

            ans = [grid, difficulty]

            hardest_generate.append(ans)

        hardest_generate.sort(key=lambda x: x[1], reverse=True)
        
        self.ans = transfer_grid(hardest_generate[0][0], 2, 1) 

    def generate_complete(self,grid_inp):

        #Create grid
        grid = transfer_grid(grid_inp, 1, 2)

        cord_locs = [[i,j] for i in range(9) for j in range(9)]

        while True:

            #Place random number in grid
            #If grid has 0 solutions, edit and continue
            #If grid has 1 solution, break, unique grid found
            #If grid has 2 solutions, keep going (non-unique valid solution)

            cords = cord_locs[random.randint(0,len(cord_locs)-1)]

            if grid_inp[9*cords[0]+cords[1]]=='0':
                num = random.randint(1,9)
                grid[cords[0]][cords[1]] = num

                try:
                    self.solving(grid)

                    if self.sols==2:
                        cord_locs.remove(cords)
                    if self.sols==1:
                        return grid
                    if self.sols==0:
                        grid[cords[0]][cords[1]]=0

                except:
                    grid[cords[0]][cords[1]]=0        
    
    def remove_complete(self,grid,attempts,original):
        
        changes = 0
        #Attempt to remove cells and minimise the unique solution 
        for a in range(attempts):

            i=random.randint(0,8)
            j=random.randint(0,8)
            if original[9*i+j]!='0' or grid[i][j]==0:
                continue

            k=grid[i][j]
            grid[i][j] = 0
            self.solving(grid)

            if self.sols!=1:
                grid[i][j]=k
            else:
                changes+=1

        if attempts >= 200:

            for i in range(9):
                for j in range(9):

                    if grid[i][j] != 0 and original[9*i+j]=='0':

                        k= grid[i][j]
                        grid[i][j]=0

                        self.solving(grid)
                        if self.sols!=1:
                            grid[i][j]=k
                        
                        else:
                            changes+=1

        return [grid,changes]
    