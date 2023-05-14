import json

class BoundData():
    def __init__(self, data):
        self.width = abs(data['x2'] - data['x1'])
        self.height = abs(data['y2'] - data['y1'])
        self.x = min(data['x1'], data['x2'])
        self.y = min(data['y1'], data['y2'])

def getBoundData():
    with open('data.json') as f:
        data = json.load(f)
    return BoundData(data)
