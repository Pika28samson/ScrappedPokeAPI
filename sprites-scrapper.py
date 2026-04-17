import json
import os
import requests
from PIL import Image
from io import BytesIO
from pathlib import Path

cwd = r"C:\Me\Python Projects\All Pokemon Sprites"
file_path = os.path.join(cwd, "all_pokemon_forms.json")
#file_path = os.path.join(cwd, "bulbasaur-test.json")

# Step 1: Open and read JSON file
with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

def addpic(cur_dict, parent_path):
    for key in cur_dict.keys():
        val = cur_dict[key]
        if not val:
            continue
            
        path = os.path.join(parent_path, key)
        
        if isinstance(val, dict):
            addpic(val, path)
        #else:
        elif Path(os.path.join(path, val.split("/")[-1])).exists():
            print("Skipped "+str(os.path.join(path, val.split("/")[-1])))
        else:
            # Extract image name from URL
            img_name = val.split("/")[-1]
            Path(path).mkdir(parents=True, exist_ok=True)

            print(f"Downloading: {val}")
            try:
                response = requests.get(val, timeout=10)
                if response.status_code == 200:
                    save_path = os.path.join(path, img_name)
                    
                    # Save the raw bytes (works for PNG, JPG, AND SVG)
                    with open(save_path, "wb") as file:
                        file.write(response.content)
                    
                    # Only use Pillow for previewing non-SVG files
                    if not img_name.lower().endswith('.svg'):
                        img = Image.open(BytesIO(response.content))
                        # img.show() # Optional: showing every image might be slow/annoying
                    else:
                        print(f"SVG saved: {img_name} (Pillow preview skipped)")
                else:
                    print(f"Failed to download {val}, status: {response.status_code}")
            except Exception as e:
                print(f"Error processing {val}: {e}")


for i in data.keys():
    addpic(data[i]["sprites"],os.path.join(cwd, "sprites"))
print("DONE")