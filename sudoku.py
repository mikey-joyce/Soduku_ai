import time
import numpy
from functools import reduce

class Sudoku():
    def __init__(self, input):
        '''initialize variables this class needs'''
        self.slices = [slice(0,3), slice(3,6), slice(6,9)]
        a,b,c = self.slices
        self.allgrids=[(si,sj) for si in [a,b,c] for sj in [a,b,c]]
        self.FULLDOMAIN = numpy.array(range(1,10)) 
        self.board = Sudoku.toBoard(input)
        self.count = 0

    def toBoard(input):
        '''Turns the input into a sudoku board'''
        return numpy.array([int(s) for s in list(input)]).reshape((9,9))

    def getGrid(self, var):
        '''Returns the 3x3 sections of the sudoku board'''
        row,column = var
        section = (self.slices[int(row/3)], self.slices[int(column/3)] )
        return section

    # Constraints
    def unique_rows(self):
        '''Checks to see if the rows are unique'''
        for row in self.board:
            if not numpy.array_equal(numpy.unique(row),numpy.array(range(1,10))) :
                return False
        return True

    def unique_columns(self):
        '''Checks to see if the columns are unique'''
        for row in self.board.T: #transpose soduku to get columns
            if not numpy.array_equal(numpy.unique(row),numpy.array(range(1,10))) :
                return False
        return True

    def unique_sections(self):
        '''Checks to see if the 3x3 sections are unique'''
        for grid in self.allgrids: 
            if not numpy.array_equal(numpy.unique(self.board[grid]),numpy.array(range(1,10))) :
                return False
        return True

    def finished(self):
        '''Checks to see if the sudoku board is done being solved'''
        if 0 in self.board:
            return False
        else:
            return True

    def result(self):
        '''Checks to see if the sudoku board has been correctly solved'''
        if self.unique_columns():
            if self.unique_rows():
                if self.unique_sections():
                    return True
        return False

    # Search
    def domain(self, target):
        '''gets the domain for the backtracking algorithm'''
        row,column = target
        temp = reduce(numpy.union1d, (self.board[row,:], self.board[:,column], self.board[self.getGrid(target)]))
        available = numpy.setdiff1d(self.FULLDOMAIN, temp)
        return available

    def getMinRemainVals(self, values):
        '''The minimum remaining value heuristic function'''
        domains = [self.domain(val) for val in values]
        sizes = [len(node) for node in domains]
        index = numpy.argmin(sizes)
        return values[index], domains[index]

    def backtrack(self):
        "Backtracking search algorithm"
        #If board has been completed then return the answer
        if self.finished():
            return self.board

        #Get the MRV heuristic
        indices = [tuple(e) for e in numpy.transpose(numpy.where(self.board==0))]
        index, available = self.getMinRemainVals(indices)
        
        #backtrack main algorithm
        for node in available:
            if self.count < 4:
                print("Variable Selected: ", index)
                print("Domain Size: ", len(available))
                print("Value Assigned: ", node)
                self.count += 1
            self.board[index] = node
            result = self.backtrack()
            if numpy.any(result):
                return result
            else:
                self.board[index] = 0
        return False

# Inputs
start = time.time()
board_a = "001002000005006030460005000000104000600800143000090508800049050100320000009000300"
print("Board A input:", board_a)
a = Sudoku(board_a)

# Solve board a
print("solved a:\n", a.backtrack())
print("Execution time: ", time.time() - start)
print("correct:", a.result())

print()
print()

start = time.time()
board_b = "005010000002004030109000206200030000040000700500007001000603000060100000000070050"
print("Board B input:", board_b)
b = Sudoku(board_b)

#solve board b
print("solved b:\n", b.backtrack())
print("Execution time: ", time.time() - start)
print("correct:", b.result())

print()
print()

start = time.time()
board_c = "670000000025000000090560200300080900000000801000470000008600090000000010106050070"
print("Board C input:", board_c)
c = Sudoku(board_c)

#solve board c
print("solved c:\n", c.backtrack())
print("Execution time: ", time.time() - start)
print("correct:", c.result())
