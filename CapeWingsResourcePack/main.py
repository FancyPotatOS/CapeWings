
import os
import shutil
from PIL import Image


def get_brightness(color):
    return color[0] + color[1] + color[2]


def get_palette(filename):
    img = Image.open(filename).convert("RGBA")

    palette = []
    for x in range(img.width):
        for y in range(img.height):
            color = img.getpixel((x, y))
            if color[3] != 0 and not color in palette:
                palette.append(color)
    
    palette.sort(key=get_brightness)
    
    return palette



ELYTRA_PALETTE = get_palette("elytra.png")
ELYTRA_ITEM_PALETTE_SIZE = len(ELYTRA_PALETTE)

WOOL_ITEMS = [
    "white_wool",
    "orange_wool",
    "magenta_wool",
    "light_blue_wool",
    "yellow_wool",
    "lime_wool",
    "pink_wool",
    "gray_wool",
    "light_gray_wool",
    "cyan_wool",
    "purple_wool",
    "blue_wool",
    "brown_wool",
    "green_wool",
    "red_wool",
    "black_wool",
    "white_carpet",
    "orange_carpet",
    "magenta_carpet",
    "light_blue_carpet",
    "yellow_carpet",
    "lime_carpet",
    "pink_carpet",
    "gray_carpet",
    "light_gray_carpet",
    "cyan_carpet",
    "purple_carpet",
    "blue_carpet",
    "brown_carpet",
    "green_carpet",
    "red_carpet",
    "black_carpet",
    "white_dye",
    "orange_dye",
    "magenta_dye",
    "light_blue_dye",
    "yellow_dye",
    "lime_dye",
    "pink_dye",
    "gray_dye",
    "light_gray_dye",
    "cyan_dye",
    "purple_dye",
    "blue_dye",
    "brown_dye",
    "green_dye",
    "red_dye",
    "black_dye",
]

### Take the names of capewings:textures/entity/equipment/wings/*.png to make the other files:
## capewings:equipment/*.json
## capewings:items/*.json

cape_names = [f.replace(".png", "") for f in os.listdir("assets/capewings/textures/entity/equipment/wings") if f.endswith(".png")]

relative_pngs = {}

for name in cape_names:
    relative_pngs[name] = f"assets/capewings/textures/entity/equipment/wings/{name}.png"

equipment_format = """{
  "layers": {
    "wings": [
      {
        "texture": "capewings:_NAME_",
        "use_player_texture": true
      }
    ]
  }
}"""

item_model_format = """{
  "model": {
    "type": "minecraft:model",
    "model": "capewings:item/_NAME_"
  }
}"""

model_format = """{
  "parent": "minecraft:item/generated",
  "textures": {
    "layer0": "capewings:item/_NAME_"
  }
}"""

recipe_format_old = """{
  "type": "minecraft:crafting_transmute",
  "ingredient": "",
  "category": "misc",
  "input": "minecraft:elytra",
  "material": "minecraft:_ITEM_",
  "result": {
    "id": "minecraft:elytra",
    "components": {
      "minecraft:item_model": "capewings:_NAME_",
      "minecraft:equippable": {
        "slot": "chest",
        "equip_sound": "minecraft:item.armor.equip_elytra",
        "asset_id": "capewings:_NAME_",
        "dispensable": true,
        "swappable": true,
        "damage_on_hurt": false,
        "equip_on_interact": true,
        "can_be_sheared": false
      },
      "minecraft:item_name": {
        "text": "_PROPERNAME_ Elytra",
        "italic": false
      }
    },
    "count": 1
  }
}"""

recipe_format = """{
  "type": "minecraft:smithing_transform",
  "base": "minecraft:elytra",
  "addition": "minecraft:_ITEM_",
  "template": "#minecraft:wool",
  "result": {
    "id": "minecraft:elytra",
    "components": {
      "minecraft:item_model": "capewings:_NAME_",
      "minecraft:equippable": {
        "slot": "chest",
        "equip_sound": "minecraft:item.armor.equip_elytra",
        "asset_id": "capewings:_NAME_",
        "dispensable": true,
        "swappable": true,
        "damage_on_hurt": false,
        "equip_on_interact": true,
        "can_be_sheared": false
      },
      "minecraft:item_name": {
        "text": "_PROPERNAME_ Elytra",
        "italic": false
      }
    },
    "count": 1
  }
}"""

item_index = 0
for name in cape_names:
    with open(f"assets/capewings/equipment/{name}.json", "w") as file:
        file.write(equipment_format.replace("_NAME_", name))
        
    with open(f"assets/capewings/items/{name}.json", "w") as file:
        file.write(item_model_format.replace("_NAME_", name))
        
    with open(f"assets/capewings/models/item/{name}.json", "w") as file:
        file.write(model_format.replace("_NAME_", name))
    
    with open(f"assets/capewings/recipes/{name}.json", "w") as file:
        file.write(recipe_format.replace("_NAME_", name).replace("_PROPERNAME_", name.title()).replace("_ITEM_", WOOL_ITEMS[item_index]))
    
    palette = get_palette(relative_pngs[name])
    target_image_name = f"assets/capewings/textures/item/{name}.png"

    new_palette = []
    for i in range(ELYTRA_ITEM_PALETTE_SIZE):
        new_palette.append(palette[int(len(palette) * (1.0 * i / ELYTRA_ITEM_PALETTE_SIZE))])
    palette = new_palette

    if name == "copper":
        continue

    shutil.copyfile("elytra.png", target_image_name)

    img = Image.open(target_image_name).convert("RGBA")

    for x in range(img.width):
        for y in range(img.height):
            color = img.getpixel((x, y))

            if color[3] == 0:
                continue

            index = ELYTRA_PALETTE.index(color)
            
            img.putpixel((x, y), palette[index])
    
    img.save(target_image_name)

    item_index += 1
    
