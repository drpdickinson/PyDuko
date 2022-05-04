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
    def InitialSet(self, val):
        self.has_value = True
        self.value = val
        self.possibles.clear()
        self.possibles.append(val)

    #eliminates a possible, and may set value
    def Eliminate(self, poss):
        if(self.has_value): return False #already set
        self.possibles.remove(poss) #remove the specified value
        if(len(self.possibles)>1): return False #more than 1 still left
        self.value=possibles[0] #setting value
        self.has_value = True
        return True #has set self

##########################################################
# Class definition for the whole map
##########################################################
class cSoduMap:
    def __init__(self):
        ##class variables
        self.grid = []
        self.rows = []
        self.cols = []
        self.boxes = []

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
        return (self.ColumnNumber(gridIndex) % 3) + ((self.RowNumber(gridIndex) % 3)*3)

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

        for i in range(81):
            val = int(initset[i])
            if ( val > 0 and val<10):
                self.grid[i].InitialSet(val)
            elif val != 0:
                print('Data invalid at element '+str(val))
                return false

        sudofile.close()
        return True

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
                print('|   |   |   |')

    def Save(self):
        print('to do')

    def SolveDeductive(self):
        print('to do')
        #





    def SolveBacktrack(self):
        print('to do')


