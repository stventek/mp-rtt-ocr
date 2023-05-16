import json

def scale_json(json_data, scale):
    scaled_json = json_data.copy()

    for key, value in json_data.items():
        if isinstance(value, dict):
            scaled_json[key] = scale_json(value, scale)
        elif isinstance(value, list):
            scaled_json[key] = [scale_size(size, scale) for size in value]
        elif isinstance(value, int):
            scaled_json[key] = scale_size(value, scale)

    return scaled_json

def scale_size(size, scale):
    if isinstance(size, int):
        return size * scale
    elif isinstance(size, str) and size.isdigit():
        return str(int(size) * scale)
    else:
        return size

# Load the JSON file
with open('custom_theme.json') as file:
    json_data = json.load(file)

# Define the desired scale factor
scale_factor = 1.4

# Scale the JSON data
scaled_data = scale_json(json_data, scale_factor)

# Print the scaled JSON
print(json.dumps(scaled_data, indent=2))
