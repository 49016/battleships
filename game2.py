import numpy as np
from ast import literal_eval
from numpy.lib.stride_tricks import sliding_window_view
import random 
import secrets
class Board:
    def __init__(self,width,height):
        """ Nothing is 0 a ship is 1 a killed ship is -1 and an water hit is -2 """
        self.map= np.zeros((width,height),dtype=int)
        random.seed(secrets.token_bytes(5))

    def populateBoard(self,ships=[2,3,3,4,5]):
        if ships==[]:
            return 
        shi = ships.pop()
        possibleSpots = sliding_window_view(self.map, (3, shi+2),writeable=True) 
        possibleSpots = [item for row in possibleSpots for item in row]
        secondSpots= sliding_window_view(self.map, (2+shi,3),writeable=True)
        secondSpots= [item for row in secondSpots for item in row]
        possibleSpots +=secondSpots
        random.seed(secrets.token_bytes(10))
        random.shuffle(possibleSpots)
        for spo in possibleSpots:
            if spo.any():
                continue 
            spo[1:-1,1:-1]+=1
            break
        else:
            print("something went wrong")
        self.populateBoard(ships)

    def inBounds(self,x,y):
        W,H = self.map.shape
        if 0>x or W<=x:
            return False 
        if 0>y or H<=y:
            return False
        return True

    def getField(self,x,y):
        if self.inBounds(x,y):
            return self.map[x][y]
        return False


    def existsPart(self,x,y):
        surr = [(x+1,y),(x,y+1),(x-1,y),(x,y-1)]
        return len(list(filter(lambda x: self.getField(*x)==1, filter(lambda x: self.inBounds(*x),surr)))) >0
    def hit(self,x,y):
        """returns true iff a alive ship was hit"""
        if not self.inBounds(x,y):
            return False
        if self.getField(x,y) == 1:
            self.map[x][y] = -1 
            if self.existsPart(x,y):
                return True 
            return "SUNK"
        if self.getField(x,y) == -1:
            return False
        if self.getField(x,y) == 0:
            self.map[x][y] = -2
            return False

    def getPublicBoard(self):
        ret = self.map
        return ret.clip(-3,0)
class GameBroker:
    def __init__(self,w=10,h=10,ships=[2,3,3,4,5]):
        self.board = Board(w,h)
        self.board.populateBoard(ships.copy())
        self.shoots = 0
        self.targets = []
        assert np.sum(self.board.map) == sum(ships),f"Real is {np.sum(self.board.map)} instead of {sum(ships)}"

    def isWon(self):
        return not any(map(lambda x: x==1,self.board.map.flatten()))

    def getBoard(self):
        return self.board.getPublicBoard()
    
    def shoot(self,x,y):
        if not self.inBounds(x,y):
            return False 
        if  self.isWon():
            return False
        if (x,y) in self.targets:
            return False
        self.shoots +=1 
        self.targets += [(x,y)]
        return self.board.hit(x,y)
    
    def alreadyShot(self,x,y):
        return (x,y) in self.targets

    def inBounds(self,x,y):
        return self.board.inBounds(x,y)

if __name__ == "__main__":
    tshot = 0 
    for i in range(500):
        game = GameBroker()
        while not game.isWon():
            print(game.getBoard())
            target = literal_eval(input("give me your target please"))
            if game.shoot(*target):
                print("nice a hit")
            else:
                print("unlucky")
        print(f"Nice you won it took you {game.shoots} to win")
        tshot +=game.shoots
    if tshot < 25000:
        print("nice here you got a FLAG")
        print("GPNCTF{IDK_PLEASE_HELP_ME")
