import sys
import numpy as np
from functools import reduce

class Sudoku():
    def __init__(self, input):
        self.slices = [slice(0,3), slice(3,6), slice(6,9)]
        s1,s2,s3 = self.slices
        self.allgrids=[(si,sj) for si in [s1,s2,s3] for sj in [s1,s2,s3]] # Makes 2d slices for grids
        self.FULLDOMAIN = np.array(range(1,10)) #All possible values (1-9)
        self.board = Sudoku.toBoard(input)

    def toBoard(input):
        "Converts string to 2d array"
        return np.array([int(s) for s in list(input)]).reshape((9,9))

    def getGrid(self, var):
        "Returns the grid slice (3x3) to which the variable's coordinates belong "
        row,col = var
        grid = (self.slices[int(row/3)], self.slices[int(col/3)] )
        return grid

    # Constraints
    def unique_rows(self):
        for row in self.board:
            if not np.array_equal(np.unique(row),np.array(range(1,10))) :
                return False
        return True

    def unique_columns(self):
        for row in self.board.T: #transpose soduku to get columns
            if not np.array_equal(np.unique(row),np.array(range(1,10))) :
                return False
        return True

    def unique_grids(self):
        for grid in self.allgrids: 
            if not np.array_equal(np.unique(self.board[grid]),np.array(range(1,10))) :
                return False
        return True

    def finished(self):
        if 0 in self.board:
            return False
        else:
            return True

    def result(self):
        if self.unique_columns():
            if self.unique_rows():
                if self.unique_grids():
                    return True
        return False


    # Search
    def domain(self, var):
        "Gets the remaining legal values (available domain) for an unfilled box `var` in `soduku`"
        row,col = var
        used_d = reduce(np.union1d, (self.board[row,:], self.board[:,col], self.board[self.getGrid(var)]))
        avail_d = np.setdiff1d(self.FULLDOMAIN, used_d)
        #print(var, avail_d)
        return avail_d

    def getMinRemainVals(self, vars):
        """
        Returns the unfilled box `var` with minimum remaining [legal] values (MRV) 
        and the corresponding values (available domain)
        """
        avail_domains = [self.domain(var) for var in vars]
        avail_sizes = [len(avail_d) for avail_d in avail_domains]
        index = np.argmin(avail_sizes)
        return vars[index], avail_domains[index]

    def backtrack(self):
        "Backtracking search to solve soduku"
        # If soduku is complete return it.
        if self.finished():
            return self.board
        # Select the MRV variable to fill
        vars = [tuple(e) for e in np.transpose(np.where(self.board==0))]
        var, avail_d = self.getMinRemainVals(vars)
        # Fill in a value and solve further (recursively), 
        # backtracking an assignment when stuck
        for value in avail_d:
            self.board[var] = value
            result = self.backtrack()
            if np.any(result):
                return result
            else:
                self.board[var] = 0
        return False

# Inputs
board_a = "001002000005006030460005000000104000600800143000090508800049050100320000009000300"
print("Board A input:", board_a)
a = Sudoku(board_a)

# Solve board a
print("solved a:\n", a.backtrack())
print("correct:", a.result())


board_b = "005010000002004030109000206200030000040000700500007001000603000060100000000070050"
print("Board B input:", board_b)
b = Sudoku(board_b)

#solve board b
print("solved b:\n", b.backtrack())
print("correct:", b.result())


board_c = "670000000025000000090560200300080900000000801000470000008600090000000010106050070"
print("Board C input:", board_c)
c = Sudoku(board_c)

#solve board c
print("solved c:\n", c.backtrack())
print("correct:", c.result())
