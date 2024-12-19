from typing import Tuple,List
import random
import numpy as np
class Ship:
    def __init__(self,name:str,positions:List[Tuple[int,int]]):
        self.positions = positions
        self.name = name 
        self.health = {i:1 for i in positions}
    
    def isAlive(self)->bool:
        return any(self.health.values())
    
    def check_empty(self,pos:Tuple[int,int])->bool:
        if self.health.get(pos,False):
            return False 
        return True

    def hit(self,pos:Tuple[int,int])->bool:
        if self.health.get(pos,False):
            self.health[pos] = 0
            return True
        return False
def randomDirection()->Tuple[int,int]:
    return random.choice([(0,1),(1,0),(-1,0),(0,-1)])

class Board:
    def __init__(self,width:int,height:int):
        self.width = width
        self.height= height
        self.ships = []

    def addShip(self,ship:Ship):
        self.ships.append(ship)

    def check_health(self,pos:Tuple[int,int])->int:
        """-1 empty 0 hit 1 healthy"""
        for sh in self.ships:
            for quart in sh.positions:
                if quart == pos:
                    return 0 if sh.check_empty(pos) else 1
        return -1 
    

    def check_empty(self,pos:Tuple[int,int])->bool:
        """returns true if hit ship"""
        for sh in self.ships:
            for quart in sh.positions:
                if quart == pos:
                    return sh.check_empty(pos)
        return True 
    
    def hit(self,pos:Tuple[int,int])->bool:
        """returns true if hit ship"""
        for sh in self.ships:
            for quart in sh.positions:
                if quart == pos:
                    return sh.hit(pos)
        return False
    
    def inBounds(self,pos:Tuple[int,int]):
        return pos[0]>=0 and pos[1]>=0 and pos[0]<=self.width and pos[1]<=self.height 


    def _randomShip(self,size:int)->Ship:
        while True:
            startPos = ( random.randint(0,self.width),random.randint(0,self.height))
            direction = randomDirection()
            if not self.inBounds((size*direction[0]+startPos[0], size*direction[1]+startPos[1])):
              #  print(startPos,"not in bounds wiht size",size,"in dir",direction, size*direction[0]+startPos[0], size*direction[1]+startPos[1])
                continue 
            pos = [(startPos[0]+i*direction[0],startPos[1]+i*direction[1]) for i in range(size)]
            if not all(list(map(self.check_empty,pos))):
                print("weird")
                continue
            return Ship(f"{size}-thing",pos)
        


    def populateBoard(self,shipSizes=[2,3,3,4,5]):
        while shipSizes!=[]:
            got = shipSizes.pop()
            self.addShip(self._randomShip(got))

    def printBoard(self):
        for y in range(self.height):
            for x in range(self.width):
                state = self.check_health((x,y))
                if state == -1:
                    print("_ ",end="")
                elif state==0:
                    print("X ",end="")
                elif state==1:
                    print("# ",end="")
            print()
    def getBoard(self):
        board = [[None for _ in range(self.height)] for _ in range(self.width)]
        for y in range(self.height):
            for x in range(self.width):
                    state = self.check_health((x,y))
                    if state == -1:
                        board[x][y] = None 
                    elif state==0:
                        board[x][y]=1
        return board

class GameBroker:
    def __init__(self):
        self.board = Board(10,10)
        self.board.populateBoard()


    def showBoardState(self):
        return self.board.getBoard()

b = Board(10,10)
s = Ship("test",[(0,0),(1,0)])
b.populateBoard()
b.printBoard()
print(b.ships[0].positions)
print(b.getBoard())
