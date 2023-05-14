import json

def computeFrameData(x1, y1, x2, y2):
    w = abs(x2 - x1)
    h = abs(y2 - y1)
    x = min(x1, x2)
    y = min(y1, y2)
    return (x, y, w, h,)

class StateData:
    def __init__(self):
        data = self._loadData()
        self.x1 = data.get('x1')
        self.x2 = data.get('x2')
        self.y1 = data.get('y1')
        self.y2 = data.get('y2')

    def _loadData(self) -> dict:
        try:
            with open('data.json') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def to_dict(self ):
        return {
            'x1': self.x1, 
            'x2': self.x2,
            'y1': self.y1,
            'y2': self.y2,
        }

    def saveState(self):
        with open('data.json', 'w') as f:
            json.dump(self.to_dict(), f)