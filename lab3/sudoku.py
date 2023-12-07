grid = [
    [7, 0, 0, 0, 3, 4, 8, 0, 0],
    [8, 0, 4, 6, 0, 0, 0, 0, 0],
    [0, 3, 9, 0, 5, 0, 0, 0, 0],
    [1, 0, 0, 5, 0, 0, 6, 0, 0],
    [0, 4, 0, 7, 0, 9, 0, 3, 0],
    [0, 0, 3, 0, 0, 8, 0, 0, 9],
    [0, 0, 0, 0, 7, 0, 3, 2, 0],
    [0, 2, 6, 0, 0, 1, 9, 0, 5],
    [0, 0, 7, 9, 2, 0, 0, 0, 4]
]
gridSize = len(grid)
areaSize = int(gridSize**0.5)


def display():
    print()
    for row in grid:
        print(row)
    print()


def posLeft():
    zeroCount = 0
    for i in range(gridSize):
        for j in range(gridSize):
            if grid[i][j] == 0:
                zeroCount += 1

    return zeroCount


zeros = posLeft()


def searchArea(areaNum, target) -> bool:
    row = (areaNum // areaSize)*areaSize
    col = (areaNum % areaSize)*areaSize
    for r in range(row, row+areaSize):
        for c in range(col, col+areaSize):

            if grid[r][c] == target:
                return True
    return False


def searchAreaByCor(row, col, target):
    startRow = row//areaSize * areaSize
    startCol = col//areaSize * areaSize

    for r in range(startRow, startRow+areaSize):
        for c in range(startCol, startCol+areaSize):

            if grid[r][c] == target:
                return False
    return True


def checkRow(row, target):
    for c in range(0, gridSize):
        if grid[row][c] == target:
            return False
    return True


def checkCol(col, target):
    for r in range(0, gridSize):
        if grid[r][col] == target:
            return False
    return True


def eliminateVertNHori(row, col):
    arr = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    for i in range(0, gridSize):
        if grid[row][i] in arr:
            arr.remove(grid[row][i])
        if grid[i][col] in arr:
            arr.remove(grid[i][col])
    return arr


def findSpots(target):
    global zeros
    possibilities = []
    for i in range(gridSize):
        if not searchArea(i, target):
            rowStart, colStart = (i // areaSize) * \
                areaSize, (i % areaSize)*areaSize
            for row in range(rowStart, rowStart+areaSize):
                for col in range(colStart, colStart+areaSize):
                    if checkRow(row, target) and checkCol(col, target) and grid[row][col] == 0:
                        possibilities.append([row, col])
            if len(possibilities) == 1:
                grid[possibilities[0][0]][possibilities[0][1]] = target
                zeros -= 1
            possibilities = []


def eliminateOptions(row, col):
    global zeros
    arr = eliminateVertNHori(row, col)
    if len(arr) == 1 and searchAreaByCor(row, col, arr[0]) and grid[row][col] == 0:
        grid[row][col] = arr[0]
        zeros -= 1


def solve():
    display()
    while zeros > 0:
        prev = zeros
        for n in range(gridSize):
            findSpots(n+1)
        if zeros == prev:
            for row in range(0, gridSize):
                for col in range(0, gridSize):
                    eliminateOptions(row, col)
    display()


zeros = posLeft()
solve()
