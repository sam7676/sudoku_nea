from imports import *

def create_grid(nums,complex=True):
    
    #Creates either 2D or 3D grid

    grid=[]

    #Removes spaces, returns if invalid
    nums=nums.replace(' ','')
    if len(nums)!=81: 
        return

    temp=[]

    #If invalid input break return nothing, otherwise return 2D / 3D grid
    for i in range(len(nums)):
        if nums[i] not in {'0','1','2','3','4','5','6','7','8','9'}:
            return
        elif complex:
            if nums[i] == '0':
                temp.append([i for i in range(1,10)])
            else:
                temp.append([int(nums[i])])
            if i%9 == 8:
                grid.append(temp)
                temp = []
        else:
            temp.append(int(nums[i]))
            if i%9==8:
                grid.append(temp)
                temp=[]
    return grid
def print_grid(grid):

    #Prints grid to terminal. Processes differently whether string or list

    if type(grid)==list:
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
    else:
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
def export_answer(grid):

    #Converts grid to 1D string answer for easier management

    ans = ''
    if type(grid[0][0])==list:
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                ans +=str(grid[i][j][0])
    else:
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                ans +=str(grid[i][j])
    return ans
def store_list(listK):

    #Makes and returns a new copy of a list without modifying the original
    #Attempted to skip this by using copy module's deepcopy, however that was not optimised and the function took longer
    #so ignored

    temp = []
    for i in range(len(listK)):
        temp2 = [listK[i][0][:],listK[i][1],listK[i][2]]
        temp.append(temp2)
    return temp
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
def get_row(grid,y1):
    return [[grid[y1][0],y1,0],[grid[y1][1],y1,1],[grid[y1][2],y1,2],[grid[y1][3],y1,3],[grid[y1][4],y1,4],[grid[y1][5],y1,5],[grid[y1][6],y1,6],[grid[y1][7],y1,7],[grid[y1][8],y1,8]]
def get_col(grid,x1):
    return [[grid[0][x1],0,x1],[grid[1][x1],1,x1],[grid[2][x1],2,x1],[grid[3][x1],3,x1],[grid[4][x1],4,x1],[grid[5][x1],5,x1],[grid[6][x1],6,x1],[grid[7][x1],7,x1],[grid[8][x1],8,x1]]
def get_box(grid,y1,x1):
    modY = y1%3
    modX = x1%3
    return [[grid[y1-(modY)][x1-(modX)],y1-(modY),x1-(modX)],[grid[y1-(modY)][x1-(modX)+1],y1-(modY),x1-(modX)+1],
            [grid[y1-(modY)][x1-(modX)+2],y1-(modY),x1-(modX)+2],[grid[y1-(modY)+1][x1-(modX)],y1-(modY)+1,x1-(modX)],
            [grid[y1-(modY)+1][x1-(modX)+1],y1-(modY)+1,x1-(modX)+1],[grid[y1-(modY)+1][x1-(modX)+2],y1-(modY)+1,x1-(modX)+2],
            [grid[y1-(modY)+2][x1-(modX)],y1-(modY)+2,x1-(modX)],[grid[y1-(modY)+2][x1-(modX)+1],y1-(modY)+2,x1-(modX)+1],
            [grid[y1-(modY)+2][x1-(modX)+2],y1-(modY)+2,x1-(modX)+2]]

class constraint:
    def __init__(x,nums):
        start_time = perf_counter()
        grid = create_grid(nums)
        x.moves,x.move_toggle=[],False
        x.ans = x.start(grid)
        x.time = perf_counter()-start_time
        print(f'Constraint solver: {round(x.time,6)}s')
    def return_cords(x,grid):
        #Returns co-ordinates of the cell with the minimal notes in it. Used for bowman
        for a in range(2,9+1):
            for i in range(len(grid)):
                for j in range(len(grid[i])):
                    if len(grid[i][j])==a:
                        return [i,j,a]
    def start_reg(x,grid):
        #Runs a process of executing all the non-bowman commands (minimise guessing)
        grid3=['a']
        while grid3!=grid:
            grid3 = store_grid(grid)
            grid = x.one_note_instance(grid)
            grid = x.remove_notes(grid)
            if grid3==grid:
                grid = x.partner(grid)
        return grid
    def start(x,grid,layer=0):
        #Solves sudoku. If regular solution not possible, uses bowman to guess note and re-runs
        grid = x.start_reg(grid)

        if x.check_complete(grid)==True:
            return export_answer(grid)
        
        if x.check_valid(grid)==True:
            y1,x1, num = x.return_cords(grid)
            for n in range(num):
                g = store_grid(grid)
                x.find_change_bowman(y1,x1,g[y1][x1],[g[y1][x1][n]],layer)
                g[y1][x1]=[g[y1][x1][n]]

                #If it is not the final answer, but still works, we do this step again recursively
                ans = x.start(g,layer+1) 
                if ans!=None:
                    return ans   
    def apply_changes(x,grid,LX):
        # Appends all changes of a row, column and box to the general grid
        for i in range(len(LX)):
            grid[LX[i][1]][LX[i][2]] = LX[i][0]
        return grid
    def check_complete(x,grid):
        #checks grid to see if its complete - length of all cells = 1.
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if len(grid[i][j])!=1:
                    return False
        return True
    def check_valid(x,grid):
        # Checks the validity of the grid and 
        # whether there are any cells that are empty and therefore invalid
        for i in range(len(grid)):
            for j in range(len(grid)):
                if grid[i][j] == []:
                    return False
        return True
    def apply_to_cells(x,grid,func):
        #Get all co-ordinates that mention every row, column and box
        cords = [[0,0],[3,1],[6,2],[1,3],[4,4],[7,5],[2,6],[5,7],[8,8]]
        
        for cord in cords:
            y1,x1=cord[0],cord[1]
            row = get_row(grid,y1)
            grid = func(grid,row)
            col = get_col(grid,x1)
            grid = func(grid,col)
            box = get_box(grid,y1,x1)
            grid = func(grid,box)
        return grid 
    def remove_notes(x,grid):
        #Removes notes where applicable from a given list
        def removeNote(grid,listA):
            list_store=store_list(listA)

            # For each item in cell R/C/B, if item length is 1,
            # remove instances of that number from other cells
            for i in range(len(listA)): 
                if len(listA[i][0])==1:
                    for j in range(len(listA)):
                        if i!=j and listA[i][0][0] in listA[j][0]:
                            listA[j][0].remove(listA[i][0][0])
            
            # If changes have been made, add it to the list of moves and modify grid
            if listA!=list_store:
                x.find_change(list_store,listA,4)
                return x.apply_changes(grid,listA)
            # If not return grid
            return grid
        
        return x.apply_to_cells(grid,removeNote)
    def one_note_instance(x,grid):
        #Finds instances where a number fits into only one cell in a lsit
        def noteInstance(grid,listA):
            list_store=store_list(listA)

            #If a number can fit into only one cell in a list, remove other notes from that cell
            for i in range(1,10):
                c=0
                for j in range(len(listA)):
                    if i in listA[j][0]:
                        c+=1
                if c==1:
                    for j in range(len(listA)):
                        if i in listA[j][0]:
                            listA[j][0] = [i]
            
            #If any changes have occurred, modify grid and add to move list
            if listA!=list_store:
                x.find_change(list_store,listA,1)
                return x.apply_changes(grid,listA)
            return grid

        return x.apply_to_cells(grid,noteInstance)
    def partner(x,grid):

        #used to remove the co-ordinates given as part of a row, column, box function
        def convert_RCB_to_note(LX):
            L = LX[:]
            for i in range(len(L)):
                L[i] = L[i][0]
            return L

        #finds all "partner" cells in a list
        def partnerFunc(grid,LX):
            list_store = store_list(LX)
            nums = convert_RCB_to_note(LX) 

            #goes through each number from 1 to 9
            for a in range(1,10):

                #minimum, minimum potential nums, indexes of minimum potentials
                mini,miniPot,miniInd = 10,[],[]

                def run(potential,used,mini,miniPot,miniInd):
                    
                    #if the potential length is minimal - if len(group 1)=5, then len(group 2..)<4
                    if len(potential) < mini and len(potential) < 5:

                        for i in potential: #each member of potential list
                            for j in range(len(nums)): #original list

                                #if the potential number in loop is in one of the nums terms + index isn't used
                                if i in nums[j] and j not in used:

                                    #store the potential and used list
                                    potential_store,used_store = potential[:],used[:]

                                    #any new numbers that the cell matches the potential number and haven't been used
                                    for k in nums[j]:
                                        if k not in potential_store:
                                            potential_store.append(k)

                                    #add the list position to used indexes
                                    used_store.append(j)

                                    #if new potential has same length as used list (closed loop, no more to explore)
                                    if len(potential_store)==len(used_store):
                                        len_pot_store = len(potential_store)

                                        #if the length of potential is less than the minimum, assign minimals
                                        if len_pot_store < mini: 
                                            mini,miniPot,miniInd = len_pot_store, potential_store, used_store
                                    else:

                                        #keep exploring potential until it cuts off at 0 
                                        return run(potential_store,used_store,mini,miniPot,miniInd)
                    
                    #returns the smallest findable groups and their indexes
                    return [miniPot,miniInd]

                #runs the recursive loop
                y=run([a],[],mini,miniPot,miniInd)

                #gets the minimal potential valus and their indexes, modifies the nums list for a
                miniPot,miniInd=y[0],y[1]
                for i in range(len(nums)):
                    for j in range(len(miniPot)):
                        if miniPot[j] in nums[i] and i not in miniInd:
                            nums[i].remove(miniPot[j])

            #appends changes from nums to the original list
            for i in range(len(LX)):
                LX[i][0] = nums[i]

            #applies list changes globally
            if LX != list_store:
                x.find_change(list_store,LX,2)
                grid = x.apply_changes(grid,LX)
            return grid

        #Get all co-ordinates that mention every row, column and box.
        return x.apply_to_cells(grid,partnerFunc)
    def next_move(x,nums):
        
        #For any bowman values, only include moves where guessed note = True answer
        def flatten_layer(nums,layer):
            layer_vals = []
            for i, move in enumerate(nums):

                #if bowman of right layer
                if move[0]==3 and move[5]==layer: 
                    layer_vals.append(i)

            #if >2 values, 2 notes have been guessed, so >=1 wrong ans
            if len(layer_vals)>=2: 
                layer_vals = [i for i in range(layer_vals[0],layer_vals[-1])]
                for i in range(len(nums)-1,-1,-1):
                    if i in layer_vals:
                        nums.pop(i)
            return nums
        
        #Create grid and fetch moves
        if type(nums)==list:
            grid = nums
        else:
            grid = create_grid(nums)
        grid3 = store_grid(grid)
        x.moves=[]
        if x.check_complete(grid3)==False:
            k=x.start(grid3)

        #Flatten any bowman layers
        max_layer = max(x.moves[i][5] for i in range(len(x.moves)))
        for layer in range(max_layer+1):
            x.moves = flatten_layer(x.moves,layer)
        
        return x.moves[0]
    def find_change(x,listA,listB,num):
        #Find any changes to old list and new list and add to moves array
        for i in range(len(listA)):
            if listA[i]!=listB[i]:
                x.moves.append([num,listB[i][1],listB[i][2],listA[i][0],listB[i][0],-1])
    def find_change_bowman(x,y1,x1,g1,g2,layer):
        #Add bowman guess to moves array
        x.moves.append([3,y1,x1,g1,g2,layer])

class algorithm_x:
    def __init__(x,nums):

        # This originates from another Sudoku solver, not made by me.
        # Its benefit over my developed algorithm (above) is that it is much faster 
        # due to it being a backtrack solver and independent of solution difficulty.
        # However, I have stripped this algorithm of its solving inputs/outputs, 
        # and it is now used to calculate the number of solutions a grid has.

        # Original code:         https://www.cs.mcgill.ca/~aassaf9/python/sudoku.txt

        start_time = perf_counter()
        grid = create_grid(nums,complex=False)
        x.ans = x.solving(grid)
        print(f"Algorithm X: {round(perf_counter()-start_time,6)}s")
    def solving(x,grid): #grid, solution
        x.sols=0
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
        X, Y = x.exact_cover(X, Y)
        for i, row in enumerate(grid):
            for j, n in enumerate(row):
                if n:
                    x.select(X, Y, (i, j, n))
        for i in x.solve(X,Y,[]):
            pass
    def exact_cover(x,X, Y):
        X = {j: set() for j in X}
        for i, row in Y.items():
            for j in row:
                X[j].add(i)
        return X, Y
    def solve(x,X, Y, solution):
        if not X:
            if x.sols<2:
                x.sols+=1
                yield
        else:
            c = min(X, key=lambda c: len(X[c]))
            for r in list(X[c]):
                solution.append(r)
                cols = x.select(X, Y, r)
                for s in x.solve(X, Y, solution):
                    yield
                x.deselect(X, Y, r, cols)
                solution.pop()
                if x.sols>=2:
                    break
    def select(x,X, Y, r):
        cols = []
        for j in Y[r]:
            for i in X[j]:
                for k in Y[i]:
                    if k != j:
                        X[k].remove(i)
            cols.append(X.pop(j))
        return cols
    def deselect(x,X, Y, r, cols):
        for j in reversed(Y[r]):
            X[j] = cols.pop()
            for i in X[j]:
                for k in Y[i]:
                    if k != j:
                        X[k].add(i)

class generate(algorithm_x):
    def __init__(x,attempts=[0,1],grid_inp='000000000000000000000000000000000000000000000000000000000000000000000000000000000'):
        
        start_time = perf_counter()
        grid_inp = flatten(grid_inp)
        final_grid = x.generate_complete(grid_inp)

        hardest_generate = []
        for i in range(attempts[1]):
            ans = x.remove_complete(store_grid(final_grid),attempts[0],grid_inp)
            hardest_generate.append(ans)
        hardest_generate.sort(key=lambda x: x[1])
        
        print(f"Generator: {round(perf_counter()-start_time,6)}s")
        x.ans = export_answer(hardest_generate[0][0]) 
    def generate_complete(x,grid_inp):

        #Create grid
        grid = create_grid(grid_inp,complex=False)
        cord_locs = [[0,0],[0,1],[0,2],[0,3],[0,4],[0,5],[0,6],[0,7],[0,8],[1,0],[1,1],[1,2],[1,3],[1,4],[1,5],[1,6],[1,7],[1,8],[2,0],[2,1],[2,2],[2,3],[2,4],[2,5],[2,6],[2,7],[2,8],[3,0],[3,1],[3,2],[3,3],[3,4],[3,5],[3,6],[3,7],[3,8],[4,0],[4,1],[4,2],[4,3],[4,4],[4,5],[4,6],[4,7],[4,8],[5,0],[5,1],[5,2],[5,3],[5,4],[5,5],[5,6],[5,7],[5,8],[6,0],[6,1],[6,2],[6,3],[6,4],[6,5],[6,6],[6,7],[6,8],[7,0],[7,1],[7,2],[7,3],[7,4],[7,5],[7,6],[7,7],[7,8],[8,0],[8,1],[8,2],[8,3],[8,4],[8,5],[8,6],[8,7],[8,8]]
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
                    x.solving(grid)
                    if x.sols==2:
                        cord_locs.remove(cords)
                    if x.sols==1:
                        return grid
                    if x.sols==0:
                        grid[cords[0]][cords[1]]=0
                except:
                    grid[cords[0]][cords[1]]=0        
    def remove_complete(x,grid,attempts,original):
        
        changes = 0
        #Attempt to remove cells and minimise the unique solution 
        for a in range(attempts):
            i=random.randint(0,8)
            j=random.randint(0,8)
            if original[9*i+j]!='0' or grid[i][j]==0:
                continue
            k=grid[i][j]
            grid[i][j] = 0
            x.solving(grid)
            if x.sols!=1:
                grid[i][j]=k
            else:
                changes+=1

        if attempts >= 200:
            for i in range(len(grid)):
                for j in range(len(grid[i])):
                    if grid[i][j]!=0:
                        k= grid[i][j]
                        grid[i][j]=0
                        x.solving(grid)
                        if x.sols!=1:
                            grid[i][j]=k
                        
                        else:
                            changes+=1

        print(f'Generation changes: {changes}')
        return [grid,changes]

