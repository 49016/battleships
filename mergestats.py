import sys
import json 
import matplotlib.pyplot as plt 
def load(fname):
    with open(fname) as f:
        return json.load(f)

def makeHistogram(gameshots):
    vals = list(set(gameshots))
    return vals, [gameshots.count(i)/len(gameshots) for i in vals]
 
data = []
for i in sys.argv[1:]:
    data+=load(i)["probHunting"]
prob_x,prob_y= makeHistogram(data)

print("Avg:",sum(data)/len(data))
fig, ax = plt.subplots()
ax.plot(prob_x,prob_y,label=f"prob {len(data)}",linewidth=2)
ax.grid(True)
ax.set_xlabel("Hits to win")
ax.set_ylabel("Probabilty")
plt.legend(loc='upper left')
plt.show()
