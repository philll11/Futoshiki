# This is a cell in a Futoshiki, consisting of x, y coordinates (column and row) and a value. 
# All parameters are integers between 1..5, values can also be 0 indicating that the value is still unknown.

import copy

class cell:
    def __init__(self, row, col, val, possibles):
        self.row = row
        self.col = col
        self.val = val
        self.possibles = possibles
        
    def getRow(self):
        return self.row
    
    def setRow(self, row):
        self.row = row
        
    def getCol(self):
        return self.col
    
    def setCol(self, col):
        self.col = col
        
    def getVal(self):
        return self.val
    
    def setVal(self, val):
        self.val = val

    def getPossVals(self):
        return self.possibles

    def setPossVals(self, val):
        self.possibles = copy.deepcopy(val)

    def removePossVals(self, val):
        if val in self.possibles:
            self.possibles.remove(val)
        
    def clone(self): 
        return cell(self.row, self.col, self.val)
