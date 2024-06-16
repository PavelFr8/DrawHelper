import os
import json

# func to get save data
def get_save():
    try:
        save_path = os.path.join("saves", "save.json")
        with open(save_path) as f:
            data = json.loads(f.read())
        return data
    except Exception:
        return {
            "color": "#00ff00",
            "opacity": 50,
            "size": 10
        }

get_save()