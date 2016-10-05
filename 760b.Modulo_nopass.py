import json

class Block:
    __slots__ = ['map', 'size']
    def __init__(self, s):
        temp = s.split(',')
        self.map = []
        size = 0
        for row in temp:
            temp2 = []
            self.map.append(temp2)
            for i in range(len(row)):
                v = {'.':0, 'X':1}[row[i]]
                temp2.append(v)
                size += v

        self.size = size

        print(s)
        print(self.map, self.size)




s = '{"level":3,"modu":"2","map":["100","010","011"],"pieces":["XXX","X",".X,XX","X,X,X"]}'
data = json.loads(s)
mymap = []
for row in data['map']:
    mymap.append([int(row[i]) for i in range(len(row))])

print(mymap)

for s in data['pieces']:
    Block(s)

