import json
try:
    with open('datad.json') as f:
        data : dict = json.load(f)
except FileNotFoundError:
    data = {}
print(data)