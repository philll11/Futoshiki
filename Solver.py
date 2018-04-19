# Template for the algorithm to solve a Futoshiki. Builds a recursive backtracking solution
# that branches on possible values that could be placed in the next empty cell. 
# Initial pruning of the recursion tree - 
#       we don't continue on any branch that has already produced an inconsistent solution
#       we stop and return a complete solution once one has been found

import pygame, Snapshot, Cell, Futoshiki_IO



def solve(snapshot, screen):
    # display current snapshot
    #pygame.time.delay(200)
    Futoshiki_IO.displayPuzzle(snapshot, screen)
    pygame.display.flip()


    listOfChains = []
    chainOfConstraints = []
    for currentConstraint in snapshot.getConstraints():
        for testingConstriant in snapshot.getConstraints():
            if currentConstraint[0] == testingConstriant[1]:
                chainOfConstraints.append(currentConstraint)
                chainOfConstraints.append(testingConstriant)
                if findConstraints(snapshot, chainOfConstraints, testingConstriant):
                    listOfChains.append(chainOfConstraints)
                    chainOfConstraints = []
                else:
                    chainOfConstraints = []


    # if current snapshot is complete ... return a value
    if isComplete(snapshot) and checkConsistency(snapshot):
       return True
    # The code block below handles singleton selection
    unsolved = snapshot.unsolvedCells()
    # Sorts the unsolved list of cells so that the singletons can be dealt with first
    sortedUnsolved = sorted(unsolved, key=lambda cell: len(cell.possibles))
    emptyCell = sortedUnsolved[0]
    if len(emptyCell.getPossVals()) == 1:
        newsnapshot = snapshot.clone()
        newsnapshot.setCellVal(emptyCell.getRow(), emptyCell.getCol(), emptyCell.getPossVals()[0])

        if checkConsistency(newsnapshot):
            success = solve(newsnapshot, screen)
            if success:
                return True
        return False

    #unsolved = snapshot.unsolvedCells()
    emptyCell = unsolved[1]

    # This loop will cycle through every potential value in each cell
    for val in range(5):
        # Checks whether the potential value has been placed in the row or column.
        if snapshot.notContains(emptyCell.getRow(), emptyCell.getCol(), val + 1):
            newsnapshot = snapshot.clone()
            newsnapshot.setCellVal(emptyCell.getRow(), emptyCell.getCol(), val + 1)

            if checkConsistency(newsnapshot):
                success = solve(newsnapshot, screen)
                if success:
                    return True
    return False


def findConstraints(snapshot, constraintList, currentConstraint):
    if len(constraintList) == 3:
        return True
    else:
        constraints = snapshot.getConstraints()
        for constraint in constraints:
            if currentConstraint[0] == constraint[1]:
                constraintList.append(constraint)
                if findConstraints(snapshot, constraintList, constraint):
                    return True
        return False


# def chainCheck(snapshot):



# Check whether a snapshot is consistent, i.e. all cell values comply
# with the Futoshiki rules (each number occurs only once in each row and column,
# no "<" constraints violated).
def checkConsistency(snapshot):
    constraints = snapshot.getConstraints()
    for i in constraints:
        # Extracting the less than and greater than constraints
        greaterThanConstraint = snapshot.getCellVal(i[1][0], i[1][1])
        lessThanConstraint = snapshot.getCellVal(i[0][0], i[0][1])

        # Great than constraint can not equal 1 because nothing no legal value can be less than 1
        # therefore we may as well return that the current snapshot is an invalid solution
        if greaterThanConstraint == 1 or lessThanConstraint == 5:
            return False

        # If either the greater than constraint or the less than constraint are equal to 0 then the board is not
        # finished. We may as well return true to let the program continue filling al the squares.
        # this is to prevent checking constraints that aren't assigned values yet.
        if greaterThanConstraint == 0 or lessThanConstraint == 0:
            return True

        # The greater than constraint can not be less than the less than constraint
        # If so then the board illegal
        if greaterThanConstraint <= lessThanConstraint:
            return False
    return True


# Check whether a puzzle is solved.
# return true if the Futoshiki is solved, false otherwise
def isComplete(snapshot):
    if len(snapshot.unsolvedCells()) == 0:
        for i in range(5):
            rowSolution = [1, 2, 3, 4, 5]
            colSolution = [1, 2, 3, 4, 5]
            for cell in snapshot.cellsByRow(i):
                # If this if statement is entered, there are two of the same values in current row
                if cell.getVal() not in rowSolution:
                    return False
                rowSolution.remove(cell.getVal())
            for cell in snapshot.cellsByCol(i):
                # If this if statement is entered, there are two of the same values in current column
                if cell.getVal() not in colSolution:
                    return False
                colSolution.remove(cell.getVal())
        return True
    return False




