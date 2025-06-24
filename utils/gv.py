data = {}

def set(key, value):
    global data
    data[key] = value

def get(key, default=None):
    return data.get(key, default)
