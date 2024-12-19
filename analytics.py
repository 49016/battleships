import matplotlib.pyplot as plt
from numpy.lib.stride_tricks import sliding_window_view
import sys
from game2 import * 
from rich.progress import track
import random
from numba import jit,njit,prange
import json
DIRECTIONS= [np.array([1,0],dtype=int), np.array([0,1],dtype=int), np.array([-1,0],dtype=int),np.array([0,-1],dtype=int)]

def smartRandomHitting():
    game = GameBroker()
    possible = [(i,j) for i in range(10) for j in range(10) if (i+j)%2==0]
    print(possible)
    while not game.isWon():
        pos = random.choice(possible)
        possible.remove(pos)
        game.shoot(*pos)
    return game.shoots
def hunting():
    game = GameBroker()
    possible = [(i,j) for i in range(10) for j in range(10) if (i+j)%2==0]
    while not game.isWon():
        try:
            pos = random.choice(possible)
        except IndexError:
            print(game.board.map)
            sys.exit(1)
        possible.remove(pos)
        pos = np.array(pos)
        if game.shoot(*pos):
            #hit a ship start hunting
            random.shuffle(DIRECTIONS)
            for d in DIRECTIONS:
                if game.inBounds(*(cur:=(d+pos))):
                    while game.shoot(*cur):
                        for odir  in DIRECTIONS:
                            if np.dot(odir,d):
                                continue
                            possible.append(tuple(cur+odir))
                        cur = cur + d
                        if game.isWon():
                            return game.shoots
                        #we found ship and destroyed it
    return game.shoots 
@jit(fastmath=True)
def getMostLikely(board,possible,ships):
    board = board.copy()
    counts = {p:0 for p in possible}
    tags = {p:5**p[0]*11**p[1] for p in possible}
    possible = list(set(possible))
    for p in possible:
        board[*p]=tags[p]
    
    for ship_num in prange(len(ships)):
        p_ship = ships[ship_num]
        views = sliding_window_view(board,(p_ship,1))
        views = [j for i in views  for j in i]
        views1=sliding_window_view(board,(1,p_ship))
        views1 = [j for i in views1  for j in i]
        for p in possible:
            counts[p] += sum([1 for v in views if (tags[p] in v and (not -1 in v or not -2 in v)) ])  
            counts[p] += sum([1 for v in views1 if (tags[p] in v and (not -1 in v or not -2 in v)) ])  
    return sorted(counts.items(),key=lambda x:x[1],reverse=True)[0][0]

def tenarySmart():
    game = GameBroker()
    #first we hunt for a ship
    SHIP_PREF = 4
    SHIPS=[2,3,3,4,5]
    SWITCH = 4
    possible = [(i,j) for i in range(10) for j in range(10) if (i+j)%4==0]
    firstHit =0 
    while not game.isWon():
            try:
                if len(possible) == 0:
                    possible = [(i,j) for i in range(10) for j in range(10) if (i+j)%2==0]

                pos = getMostLikely(game.getBoard().copy(),possible,ships=SHIPS)
            except IndexError:
                continue
                #print(game.board.map)
                #sys.exit(1)
            possible.remove(pos)
            pos = np.array(pos)
            if hitType:=game.shoot(*pos):
                firstHit =True
                #hit a ship start hunting
                poss = list(map(lambda x: x+pos,DIRECTIONS))
                poss = [(i[0],i[1]) for i in poss if game.inBounds(*i)]
                hitCount = 1 
                if hitType == "SUNK":
                    break

                while len(poss)>0:

                    cur = getMostLikely(game.getBoard().copy(),poss,ships=SHIPS)
                    poss.remove(cur)
                    cur = np.array(cur)
                    d = cur-pos
                    while hitType:=game.shoot(*cur):
                        hitCount+=1
                        cur = cur + d
                        if game.isWon():
                            return game.shoots
                        if hitType == "SUNK":
                            break
                SHIPS.remove(hitCount)
                        #we found ship and destroyed it
    return game.shoots 


def customSmart():
    game = GameBroker()
    #first we hunt for a ship
    SHIP_PREF = 4
    SHIPS=[2,3,3,4,5]
    SWITCH = 4
    possible = [(i,j) for i in range(10) for j in range(10) if (i+j)%1==0]
    firstHit =0 
    while not game.isWon():
            try:
                if len(possible) == 0:
                    possible = [(i,j) for i in range(10) for j in range(10) if (i+j)%2==0]

                pos = getMostLikely(game.getBoard().copy(),possible,ships=SHIPS)
            except IndexError:
                print(game.board.map)
                sys.exit(1)
            possible.remove(pos)
            pos = np.array(pos)
            if hitType:=game.shoot(*pos):
                firstHit =True
                #hit a ship start hunting
                poss = list(map(lambda x: x+pos,DIRECTIONS))
                poss = [(i[0],i[1]) for i in poss if game.inBounds(*i)]
                hitCount = 1 
                if hitType == "SUNK":
                    break

                while len(poss)>0:

                    cur = getMostLikely(game.getBoard().copy(),poss,ships=SHIPS)
                    poss.remove(cur)
                    cur = np.array(cur)
                    d = cur-pos
                    while hitType:=game.shoot(*cur):
                        hitCount+=1
                        cur = cur + d
                        if game.isWon():
                            return game.shoots
                        if hitType == "SUNK":
                            break
                SHIPS.remove(hitCount)
                        #we found ship and destroyed it
    return game.shoots 




def huntingMaster():
    """ works even with connected ships probability theory"""
    game = GameBroker()
    possible = [(i,j) for i in range(10) for j in range(10) if (i+j)%2==0]
    while not game.isWon():
        try:
            pos = getMostLikely(game.getBoard().copy(),possible,ships=[2,3,3,4,5])
        except IndexError:
            print(game.board.map)
            sys.exit(1)
        possible.remove(pos)
        pos = np.array(pos)
        if game.shoot(*pos):
            #hit a ship start hunting
            random.shuffle(DIRECTIONS)
            for d in DIRECTIONS:
                if game.inBounds(*(cur:=(d+pos))):
                    while game.shoot(*cur):
                        for odir  in DIRECTIONS:
                            if np.dot(odir,d):
                                continue
                            if game.inBounds(*(cur+odir)):
                                possible.append(tuple(cur+odir))
                        cur = cur + d
                        if game.isWon():
                            return game.shoots
                        #we found ship and destroyed it
    return game.shoots 

                            


def uniqueRandomHitting():
    game = GameBroker()
    possible = [(i,j) for i in range(10) for j in range(10)]
    while not game.isWon():
        pos = random.choice(possible)
        possible.remove(pos)
        game.shoot(*pos)
    return game.shoots

def randomHitting():
    game = GameBroker()
    possible = [(i,j) for i in range(10) for j in range(10)]
    while not game.isWon():
        pos = random.choice(possible)
        game.shoot(*pos)
    return game.shoots

def makeHistogram(gameshots):
    vals = list(set(gameshots))
    return vals, [gameshots.count(i)/len(gameshots) for i in vals]

if len(sys.argv)<2:
    print("defualt out")
    outpath= "stats.json"
else:
    outpath = sys.argv[1]
uniqueRandom = []
completeRandom = []
smartRandom = []
huntingHit = []
huntingHitProb = []
game = GameBroker()
game.shoot(4,6)
game.shoot(2,5)
game.shoot(2,1)
for i in track(range(10000)):
    #uniqueRandom.append(uniqueRandomHitting()) 
    #completeRandom.append(randomHitting()) 
    huntingHit.append(hunting())
    huntingHitProb.append(customSmart())
out = {"probHunting":huntingHitProb}
with open(outpath,"w") as f:
    json.dump(out,f)
unique_x ,unique_y = makeHistogram(uniqueRandom)
hunting_x ,hunting_y= makeHistogram(huntingHit)
prob_x,prob_y= makeHistogram(huntingHitProb)

fig, ax = plt.subplots()
ax.plot(unique_x, unique_y,label="unique random",linewidth=2)
ax.plot(hunting_x,hunting_y,label="hunting parity",linewidth=2)
ax.plot(prob_x,prob_y,label="hunting prob",linewidth=2)
ax.grid(True)
ax.set_xlabel("Hits to win")
ax.set_ylabel("Probabilty")
plt.legend(loc='upper left')
print("avg:",np.average(huntingHitProb))
plt.show()
