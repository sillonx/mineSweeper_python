#python .\mineSweeper.py

import os
import random

global displayedGrid
global hiddenGrid
global truthGrid

#Display array of array (max 16*16)
def graph2DArray(myArray) :
    width = len(myArray[0])
    height = len(myArray)

    if (height<1 or height>16) :
        print("Error : invalid array size")
        return 0
    for i in range (height) :
        if (len(myArray[i]) != width) :
            print("Error : invalid array size")
            return 0

    hexa = ["A","B","C","D","E","F"]
    firstRow = " │"
    for i in range (width) :
        if (i > 9) :
            j = i - 10
            firstRow += hexa[j] + "│"
        else :
            firstRow += str(i) + "│"

    middleRow = "─┼"
    lastRow = "─┴"

    for i in range (width) :
        if (i == width - 1) :
            lastRow += "─┘"
            middleRow += "─┤"
        else :
            lastRow += "─┴"
            middleRow += "─┼"

    print(firstRow)
    print(middleRow)

    for i in range (height) :
        if (i > 9) :
            j = i - 10
            display = hexa[j] + "│"
        else :
            display = str(i) + "│"
        for j in range (len(myArray[i])) :
            display = display + str(myArray[i][j]) + "│"
        print(display)
        if (i == len(myArray) - 1) :
            print(lastRow)
        else :
            print(middleRow)
    print("\n")
    return 1

#Update grid display
def refreshDisplay() :
    os.system('cls')
    print("\n"*3)
    graph2DArray(displayedGrid)

#Return array of arrays (h*w) filled with s
def fillGrid(height, width, s) :
    myGrid = []
    for i in range (height) :
        tempTab = []
        for j in range (width) :
            tempTab.append(s)
        myGrid.append(tempTab)
    return myGrid

displayedGrid = fillGrid(16, 16,"█")
hiddenGrid = fillGrid(16, 16, False)
truthGrid = fillGrid(16, 16, True)

#Return true if input is ok in mode, else false
def validInput(x,mode) :
    if (mode == "difficulty") :
        return x in ["1","2","3"]
    if (mode == "rowcol") :
        return x in ["0","1","2","3","4","5","6","7","8","9","A","a","B","b","C","c","D","d","E","e","F","f"]
    if (mode == "yesno") :
        return x in ["Y","y","N","n","1","0"]

#Set grids up depending on difficulty chosen
def createGame(difficulty) :
    if (difficulty == "1") :
        bombs = 0
        while (bombs < 20) :
            x = random.randint(0,15)
            y = random.randint(0,15)
            if (not (hiddenGrid[x][y])) :
                hiddenGrid[x][y] = True
                bombs += 1
        return 1
    if (difficulty == "2") :
        bombs = 0
        while (bombs < 40) :
            x = random.randint(0,15)
            y = random.randint(0,15)
            if (not (hiddenGrid[x][y])) :
                hiddenGrid[x][y] = True
                bombs += 1
        return 1
    if (difficulty == "3") :
        bombs = 0
        while (bombs < 60) :
            x = random.randint(0,15)
            y = random.randint(0,15)
            if (not (hiddenGrid[x][y])) :
                hiddenGrid[x][y] = True
                bombs += 1
        return 1

#Turn string into decimal
def hexaToDecimal(x) :
    if (x in ["0","1","2","3","4","5","6","7","8","9"]) :
        return int(x)
    else :
        if (x == "A" or x == "a") :
            return 10
        if (x == "B" or x == "b") :
            return 11
        if (x == "C" or x == "c") :
            return 12
        if (x == "D" or x == "d") :
            return 13
        if (x == "E" or x == "e") :
            return 14
        if (x == "F" or x == "f") :
            return 15

#Return the number of bombs around (x,y)
def calcNeighbors(x,y) :
    xNeighbors = 0
    if (hiddenGrid[x][y]) :
        return -1
    for i in range (-1,2) :
        for j in range (-1,2) :
            try:
                if (hiddenGrid[x+i][y+j]) :
                    xNeighbors += 1
            except IndexError:
                xNeighbors += 0
    return xNeighbors

#Reveal all the grid
def revealAll() :
    for i in range (16) :
        for j in range (16) :
            xNeighbors = calcNeighbors(i,j)
            if (xNeighbors == - 1) :
                displayedGrid[i][j] = "‼"
            else :
                if (xNeighbors == 0) :
                    displayedGrid[i][j] = " "
                else :
                    displayedGrid[i][j] = str(xNeighbors)

#Reveal one square and trigger veification on all neighbors
def revealOne(x,y) :
    if truthGrid[x][y] == True :
        xNeighbors = calcNeighbors(x,y)
        if (xNeighbors != 0) :
            displayedGrid[x][y] = str(xNeighbors)
            truthGrid[x][y] = False
        else :
            displayedGrid[x][y] = " "
            truthGrid[x][y] = False
            for i in range (-1,2) :
                for j in range (-1,2) :
                    try:
                        revealOne(x+i,y+j)
                    except IndexError:
                        pass

#Flag a square without revealing it
def flagSquare(x,y) :
    displayedGrid[x][y] = "◄"

#Launch the game
def run() :

    refreshDisplay()

    print("Welcome to MineSweeper !\n")
    print("\t1 • Easy")
    print("\t2 • Medium")
    print("\t3 • Hard\n")
    print("Chose difficulty level (0 to exit) :")
    difficultyLevel = input()

    if (difficultyLevel == "0") :
        return
    while (not validInput(difficultyLevel,"difficulty")) :
        print("\nWrong difficulty value\n")
        difficultyLevel = input()
        if (difficultyLevel == "0") :
            return
    createGame(difficultyLevel)

    flagMode = False
    while (hiddenGrid != truthGrid) :
        refreshDisplay()
        if (flagMode) :
            print("- FLAG MODE ON (-1 to turn off) -")
        print("Select a square :\n")
        print("# Row (-1 to flag / -2 to cancel / -3 to exit) :")
        rowPlayed = input()
        if (rowPlayed == "-1") :
            flagMode = not flagMode
            continue
        if (rowPlayed == "-2") :
            continue
        if (rowPlayed == "-3") :
            return
        while (not validInput(rowPlayed,"rowcol")) :
            print("\nWrong row value")
            rowPlayed = input()
            if (rowPlayed == "-1") :
                flagMode = not flagMode
                break
            if (rowPlayed == "-2") :
                break
            if (rowPlayed == "-3") :
                return

        if (rowPlayed in ["-1","-2","-3"]) :
            continue

        print("\n# Column (-1 to flag / -2 to cancel / -3 to exit) :")
        colPlayed = input()
        if (colPlayed == "-1") :
            flagMode = not flagMode
            continue
        if (colPlayed == "-2") :
            continue
        if (colPlayed == "-3") :
            return
        while (not validInput(colPlayed,"rowcol")) :
            print("\nWrong column value")
            colPlayed = input()
            if (colPlayed == "-1") :
                flagMode = not flagMode
                break
            if (colPlayed == "-2") :
                break
            if (colPlayed == "-3") :
                return

        if (colPlayed in ["-1","-2","-3"]) :
            continue

        x = hexaToDecimal(rowPlayed)
        y = hexaToDecimal(colPlayed)
        neighbors = calcNeighbors(x,y)
        if (not flagMode) :
            if (neighbors == -1) :
                if (displayedGrid[x][y] == "◄") :
                    print("\nYou're about to reveal a flagged square, continue ? (Y/N)")
                    proceedRes = input()
                    while (not validInput(proceedRes,"yesno")) :
                        proceedRes = input()
                    if (proceedRes in ["Y","y","1"]) :
                        revealAll()
                        refreshDisplay()
                        print("BOOM !")
                        print("You lost...\n")
                        return 0
                    else :
                        continue
                else :
                    revealAll()
                    refreshDisplay()
                    print("BOOM !")
                    print("You lost...\n")
                    return 0
            else :
                if (displayedGrid[x][y] == "◄") :
                    print("\nYou're about to reveal a flagged square, continue ? (Y/N)")
                    proceedRes = input()
                    while (not validInput(proceedRes,"yesno")) :
                        proceedRes = input()
                    if (proceedRes in ["Y","y","1"]) :
                        revealOne(x,y)
                    else :
                        continue
                else :
                    revealOne(x,y)
        else :
            flagSquare(x,y)

    refreshDisplay()
    print("CONGRATULATIONS !")
    print("You won.\n")
    return 1

run()