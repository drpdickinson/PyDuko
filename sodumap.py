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
        self.setList = [] #list of elements that have been set to specific values - used for elimination in units

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
        print("Map data initialised")

        #create box list = 9 lists of grid indices, one for each box from top-left to bottom-right
        self.boxes.append([0, 1, 2, 9, 10, 11, 18, 19, 20])
        for x in range(1,9):
            box = [y+((x%3)*3)+((x//3)*27) for y in self.boxes[0]]
            self.boxes.append(box)

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

        print(str(os.path.getsize(p)))
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
                print('Data invalid at element '+str(val))
                return false

        sudofile.close()

        # process eliminations in units resulting from initial values
        self.EliminationsFromSetList()etList()

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
            print('\n')
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
        #2. iterate through all units and check if there are any values which only occur once in each list of possible for unsolved locations - set these
        #3. Process eliminations from set cells
        self.setList.clear()
        #1
        for inx in range(80):
            if (self.grid[inx].has_value == False) and (len(self.grid[inx].possibles)==1):
                self.grid[inx].Set(self.grid[inx].possibles[0])
                self.setList.append(inx)

        #3
        EliminationsFromSetList()



#    def SolveBacktrack(self):
#        print('to do')


