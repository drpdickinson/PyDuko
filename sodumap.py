##########################################################
# (c) Patrick Dickinson, 2022
##########################################################

import os.path
from pathlib import Path

##########################################################
# Class definition for a single location in the soduko map
##########################################################
class cLocation:
    def __init__(self):
        self.has_value = False # true when value known
        self.value = 0
        self.possibles = [1,2,3,4,5,6,7,8,9]
        self.peers = []

    #initial set is used to initialise the map
    def Set(self, val):
        self.has_value = True
        self.value = val
        self.possibles.clear()

    #eliminates a possible, and may set value
    def Eliminate(self, poss):
        if(self.has_value): return False #already set
        if poss in self.possibles:
            self.possibles.remove(poss) #remove the specified value
        #if(len(self.possibles)>1): return False #more than 1 still left
        #self.value=possibles[0] #setting value
        #self.has_value = True
        #self.possibles.clear()
        return True #has set self

##########################################################
# Class definition for the whole map
##########################################################
class cSoduMap:
    def __init__(self):
        ##class variables
        self.grid = [] #list of elements 0-80 (0,0 = top left)
        self.rows = [] #list of lists of elements in each row (0=top)
        self.cols = [] #list of lists of elements in each column (0 = left)
        self.boxes = [] #list of lists of elements in each box (0 = top left)
        self.allunits = []
        self.setList = [] #list of elements that have been set to specific values - used for elimination in units
        self.solution = []

        #set up the main grid = 0-81 locations
        for x in range(81):
            elem = cLocation()
            self.grid.append(elem)

        #create row list = 9 lists of grid indices, one for each row from top to bottom
        self.rows.append([0, 1, 2, 3, 4, 5, 6, 7, 8])
        for x in range(1,9):
            row = [y+(x*9) for y in self.rows[0]]
            self.rows.append(row)

        #create column list = 9 lists of grid indices, one for each column from left to right
        self.cols.append([0, 9, 18, 27, 36, 45, 54, 63, 72])
        for x in range(1,9):
            col = [y+x for y in self.cols[0]]
            self.cols.append(col)

        #create box list = 9 lists of grid indices, one for each box from top-left to bottom-right
        self.boxes.append([0, 1, 2, 9, 10, 11, 18, 19, 20])
        for x in range(1,9):
            box = [y+((x%3)*3)+((x//3)*27) for y in self.boxes[0]]
            self.boxes.append(box)

        #create list of all units = 27 lists of grid indices, one for each row/col/box
        self.allunits = self.rows + self.cols + self.boxes

        '''print(f'{id(self.rows[0])}, {id(self.allunits[0])}')
        print(f'{id(self.cols[0])}, {id(self.allunits[9])}')
        print(f'{id(self.cols[8])}, {id(self.allunits[17])}')
        print(f'{id(self.boxes[0])}, {id(self.allunits[18])}')
        print(f'{id(self.boxes[2])}, {id(self.allunits[20])}')
        print(f'{self.rows[0][5]}, {self.allunits[0][5]}')
        print(f'{self.cols[0][1]}, {self.allunits[9][1]}')
        print(f'{self.boxes[0][2]}, {self.allunits[18][2]}')'''

        #Create peer lists for each location
        for x in range(81):
            rowNo = self.RowNumber(x)
            for row in self.rows[rowNo]:
                if row != x:
                    self.grid[x].peers.append(row)
            colNo = self.ColumnNumber(x)
            for col in self.cols[colNo]:
                if (col!=x) and (col not in self.grid[x].peers):
                    self.grid[x].peers.append(col)
            boxNo = self.BoxNumber(x)
            for box in self.boxes[boxNo]:
                if (box!=x) and (box not in self.grid[x].peers):
                    self.grid[x].peers.append(box)

        print('Map data initialised')

    ########################################################################################

    def RowNumber(self, gridIndex):
        # returns integer in range 0 to 8
        return gridIndex // 9

    def ColumnNumber(self, gridIndex):
        # returns integer in range 0 to 8
        return gridIndex % 9

    def BoxNumber(self, gridIndex):
        # returns integer in range 0 to 8, 0 = top, left; 8 = bottom right
        return (self.ColumnNumber(gridIndex) // 3) + ((self.RowNumber(gridIndex) // 3)*3)

    ########################################################################################

    def Load(self):
        p = Path('sodukotext.txt')
        if not p.is_file():
            print("File failed doesn't exist")
            return False

        #print(str(os.path.getsize(p)))
        try:
            sudofile = open(p)
        except:
            print('Open file failed')
            return False

        try:
            initset = sudofile.readline()
        except:
            print('Could not read file')
            return False

        if len(initset)<81:
            print('Data incomplete')
            return False

        self.setList.clear()
        for i in range(81):
            val = int(initset[i])
            if ( val > 0 and val<10):
                self.grid[i].Set(val)
                self.setList.append(i)
            elif val != 0:
                print('Data invalid at element '+str(i))
                return false

        #load solution
        try:
            soln = sudofile.readline()
            soln = sudofile.readline()
        except:
            print('Could not read file')
            return False
        if len(soln)<81:
            print('Soln incomplete')
            return False
        for i in range(81):
            val = int(soln[i])
            if (val > 0 and val < 10):
                self.solution.append(val)
            else :
                print('Solution invalid at element ' + str(i))
                return false

        sudofile.close()

        # process eliminations in units resulting from initial values
        self.EliminationsFromSetList()
        '''print(f'Location {0} locations {self.grid[0].possibles}')
        print(f'Location {1} locations {self.grid[1].possibles}')
        print(f'Location {2} locations {self.grid[2].possibles}')
        print(f'Location {11} locations {self.grid[11].possibles}')
        print(f'Location {20} locations {self.grid[20].possibles}')
        print(f'Location {29} locations {self.grid[29].possibles}')
        print(f'Location {31} locations {self.grid[31].possibles}')
        print(f'Location {32} locations {self.grid[32].possibles}')
        print(f'Location {33} locations {self.grid[33].possibles}')
        print(f'Location {35} locations {self.grid[35].possibles}')
        print(f'Location {47} locations {self.grid[47].possibles}')
        print(f'Location {65} locations {self.grid[65].possibles}')'''

        return True

    def EliminationsFromSetList(self):
        #set list is a list of grid locations that have been set to definitive values
        #for each location, eliminate that value from other locations in same unit (row, column, box)
        for setLoc in self.setList:
            setVal = self.grid[setLoc].value
            #print(f"Set Value {setVal} at {setLoc} \n")
            for otherLoc in self.grid[setLoc].peers:
                self.grid[otherLoc].Eliminate(setVal)
                #print(f'{otherLoc} ', end = ',')
            #print('\n')
        #all eliminations should have been done
        self.setList.clear()

    def Draw(self):
        inx = 0
        for x in range(9):
            print('|', end='')
            for y in range(3):
                for z in range(3):
                    if self.grid[inx].value == 0:
                        print('.', end='')
                    else:
                        print(self.grid[inx].value, end='')
                    inx+=1
                print('|', end='')
            print('')
            if x % 3 == 2:
                print('|---|---|---|')

    def Save(self):
        print('to do')

    def SolveDeductive(self):
        #1. iterate through all grid locations and check if any only have 1 possible left - set these
        #2. Process eliminations from set cells
        #3. iterate through all units and check if there are any values which only occur once in each list of possible for unsolved locations - set these
        #4. Process eliminations from set cells
        #5. Repeat until solved, or not

        self.setList.clear()

        done = False
        while(not done):
            #1
            for inx in range(80):
                if (self.grid[inx].has_value == False) and (len(self.grid[inx].possibles)==1):
                    print(f'Location {inx} has only one possible value, {self.grid[inx].possibles[0]}')
                    # sanity check against solution
                    if self.grid[inx].possibles[0] != self.solution[inx]:
                        print('Error in solution #1')
                    #end check
                    self.grid[inx].Set(self.grid[inx].possibles[0])
                    self.setList.append(inx)
            #2 do eliminations before phase 2, else possible lists for other locations are not up to date
            numSetIter = len(self.setList)
            if numSetIter > 0:
                self.EliminationsFromSetList()
            #3
            for unitInx, unit in enumerate(self.allunits):
                for value in range(1,10):
                    foundCount = 0
                    foundLoc = -1
                    for unitElem in unit:
                        if value in self.grid[unitElem].possibles:
                            foundCount+=1
                            foundLoc = unitElem
                    if foundCount == 1:
                        # sanity check against solution
                        if value != self.solution[foundLoc]:
                            print('Error in solution #2')
                        #end check
                        self.grid[foundLoc].Set(value)
                        self.setList.append(foundLoc)
                        print(f'found solo possibility, value {value} in location {foundLoc} using unit {unitInx}')
            #4
            numSetIter += len(self.setList)
            if(len(self.setList)) > 0:
                self.EliminationsFromSetList()
            #5
            if numSetIter > 0:
                done = True
                print('terminating: no items set this iteration')

        #end while loop
        numSet = 0;
        for x in self.grid:
            if x.has_value:
                numSet+=1
        print(f'Number of locations set {numSet}')

#    def SolveBacktrack(self):
#        print('to do')


