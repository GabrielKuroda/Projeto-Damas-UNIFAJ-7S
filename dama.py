
def printTabuleiro():
    print("--------------------------------")
    firstTime = True
    for idx,line in enumerate(tabuleiro):
        if(firstTime):
            print("   0  1  2  3  4  5  6  7")
            firstTime = False
        print(str(idx) + " " + str(line))
    print("--------------------------------")
        
def getPos(objectToFind):
    for idxLine, line in enumerate(tabuleiro):
        for idxColumn, value in enumerate(line):
            if objectToFind is value:
                return [idxLine,idxColumn]
                
def insertObject():
    tabuleiro[1][0] = 1
    
def moveObject(posH, posW, objectToMove):
    removeObject(objectToMove)
    tabuleiro[posW][posH] = objectToMove
    
def removeObject(objectToMove):
    pos = getPos(objectToMove)
    tabuleiro[pos[0]][pos[1]] = 0
    
def main():
    printTabuleiro()
    insertObject()
    printTabuleiro()
    moveObject(1,2,1)
    printTabuleiro()

if __name__ == "__main__":
    main()

    