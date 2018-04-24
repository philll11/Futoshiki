# Template for the algorithm to solve a Futoshiki. Builds a recursive backtracking solution
# that branches on possible values that could be placed in the next empty cell. 
# Initial pruning of the recursion tree - 
#       we don't continue on any branch that has already produced an inconsistent solution
#       we stop and return a complete solution once one has been found

import pygame, Snapshot, Cell, Futoshiki_IO


def solve(snapshot, screen):
    # display current snapshot
    pygame.time.delay(200)
    Futoshiki_IO.displayPuzzle(snapshot, screen)
    pygame.display.flip()

    if isComplete(snapshot) and checkConsistency(snapshot):
       return True

    # Singleton selection code block
    unsolvedCells = snapshot.unsolvedCells()
    # Sorts the unsolved list of cells
    sortedUnsolved = sorted(unsolvedCells, key=lambda c: len(c.possibles))
    emptyCell = sortedUnsolved[0]
    if len(emptyCell.getPossVals()) == 1:
        newsnapshot = snapshot.clone()
        newsnapshot.setCellVal(emptyCell.getRow(), emptyCell.getCol(), emptyCell.getPossVals()[0])
        if checkConsistency(newsnapshot):
            success = solve(newsnapshot, screen)
            if success:
                return True
        return False

    emptyCell = unsolvedCells[1]

    # Iterates through potential values in cells
    for val in range(5):
        # Checks potential values are already placed in row or column.
        if snapshot.notContains(emptyCell.getRow(), emptyCell.getCol(), val + 1):
            newsnapshot = snapshot.clone()
            newsnapshot.setCellVal(emptyCell.getRow(), emptyCell.getCol(), val + 1)
            if checkConsistency(newsnapshot):
                success = solve(newsnapshot, screen)
                if success:
                    return True
    return False


# Check whether a snapshot is consistent, i.e. all cell values comply
# with the Futoshiki rules (no "<" constraints violated).
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
            rowSol = [1, 2, 3, 4, 5]
            colSol = [1, 2, 3, 4, 5]
            for c in snapshot.cellsByCol(i):
                # If this if statement is entered, there are two of the same values in current column
                if c.getVal() not in colSol:
                    return False
                colSol.remove(c.getVal())
            for c in snapshot.cellsByRow(i):
                # If this if statement is entered, there are two of the same values in current row
                if c.getVal() not in rowSol:
                    return False
                rowSol.remove(c.getVal())
        return True
    return False




