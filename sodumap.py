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

    def ReInit(self):
        #reinitialise grid location
        self.has_value = False  # true when value known
        self.value = 0
        self.possibles = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    #initial set is used to initialise the map
    def Set(self, val):
        self.has_value = True
        self.value = val
        self.possibles.clear()

    #eliminates a possible value
    def Eliminate(self, poss):
        if(self.has_value): return False #already set
        if poss in self.possibles:
            self.possibles.remove(poss) #remove the specified value
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
        self.solution = []
        self.loadSolution = True

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

    def Load(self, fname, offset):
        p = Path(fname)
        if not p.is_file():
            print("File failed doesn't exist")
            return False

        try:
            sudofile = open(p)
        except:
            print('Open file failed')
            return False

        #read header + preceeding puzzles
        try:
            lines = 2 + (offset*3)
            for x in range(lines):
                initset = sudofile.readline()
            #next line is puzzle
            initset = sudofile.readline()

        except:
            print('Could not read file')
            return False

        if len(initset)<81:
            print('Data incomplete')
            return False

        #re initialise grid before loading
        for i in range(81):
            self.grid[i].ReInit()
        for i in range(81):
            val = int(initset[i])
            if ( val > 0 and val<10):
                self.grid[i].Set(val)
                self.EliminateFromPeers(i)
            elif val != 0:
                print('Data invalid at element '+str(i))
                return false

        #load solution
        if self.loadSolution == True:
            try:
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
        return True


    def EliminateFromPeers(self, locInx):
        # When a value has been set for a location, this function can be called to eliminate
        #that value from 'possibles' in the location's peers
        setVal = self.grid[locInx].value
        for peerLoc in self.grid[locInx].peers:
            self.grid[peerLoc].Eliminate(setVal)

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

    def SolveUsingConstrints(self):
        #1. iterate through all grid locations and check if any only have 1 possible left - set these
        #2. iterate through all units and check if there are any values which only occur once in each list of possible for unsolved locations - set these
        #3. Repeat until solved, or not

        done = False
        while(not done):
            numSetIter = 0
            #1
            for inx in range(80):
                if (self.grid[inx].has_value == False) and (len(self.grid[inx].possibles)==1):
                    print(f'Location {inx} has only one possible value, {self.grid[inx].possibles[0]}')
                    # sanity check against solution
                    if self.loadSolution == True:
                        if self.grid[inx].possibles[0] != self.solution[inx]:
                            print('Error in solution #1')
                    #end check
                    self.grid[inx].Set(self.grid[inx].possibles[0])
                    self.EliminateFromPeers(inx)
                    numSetIter+=1

            #2
            for unitInx, unit in enumerate(self.allunits):
                for value in range(1,10):
                    foundCount = 0
                    foundLoc = -1
                    for unitElem in unit:
                        if value in self.grid[unitElem].possibles:
                            foundCount+=1
                            foundLoc = unitElem
                    if foundCount == 1:
                        #check against set values in unit
                        # sanity check against solution
                        if self.loadSolution == True:
                            if value != self.solution[foundLoc]:
                                print('Error in solution #2')
                        #end check
                        self.grid[foundLoc].Set(value)
                        self.EliminateFromPeers(inx)
                        numSetIter += 1
                        print(f'found solo possibility, value {value} in location {foundLoc} using unit {unitInx}')
            #3
            if numSetIter > 0:
                done = True
                print('terminating: no items set this iteration')

        #end while loop
        numSet = 0;
        for x in self.grid:
            if x.has_value:
                numSet+=1
        print(f'Number of locations set {numSet}')

    def ValidityCheck(self):
        #iterate through each unit
        #should be exactly 1 of each digit only
        print('Validity check started')
        for unitInx, unit in enumerate(self.allunits):
            for val in range(1, 10):
                foundCount = 0
                for unitElem in unit:
                    if not self.grid[unitElem].has_value:
                        print(f"ERROR in solution, location {unitElem} not set")
                    if self.grid[unitElem].value == val:
                        foundCount += 1
                if foundCount != 1:
                    print(f"ERROR in solution, unit {unitInx} has {foundCount} occurences of {val}")
        print('Validity check completed')



