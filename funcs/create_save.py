import json
import os

# func which is make saves if json format
def create_save(widget):
    try:
        data = {
            'color': f'{widget.color.name()}',  # get the color in format #000000
            'size': widget.paint_size,
            'opacity': widget.opacity,
        }
        # print(data)
        save_path = os.path.join("saves", "save.json")
        widget.image.save('saves/save.png')
        with open(save_path, 'w') as f:
            json.dump(data, f)
    except Exception as e:
        print(e)
