
import os
import json
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont

top_left = (32, 192)
right_offset = (144, 0)
next_offset = (0, 88)

text_height = 26
text_top_left = (376, int(188 + (72 -text_height) / 2))

any_wool = Image.open("img/any_wool.png").convert("RGBA")
template = Image.open("img/template.png").convert("RGBA")

font = ImageFont.truetype("img/Minecraft.ttf", text_height)

recipe_files = os.listdir("data/capewings/recipe")
recipes = []

for recipe_file in recipe_files:
    with open(f"data/capewings/recipe/{recipe_file}", "r") as file:
        recipes.append((recipe_file.replace(".json", ""), json.loads("".join(file.readlines()))))
    
def get_name(item):
    return item[0]

def get_addition(item):
    if "carpet" in item[1]["addition"]:
        return "2carpet_" + item[1]["addition"][len("minecraft:"):-len("_carpet")]
    elif "wool" in item[1]["addition"]:
        return "1wool_" + item[1]["addition"][len("minecraft:"):-len("_wool")]
    elif "dye" in item[1]["addition"]:
        return "3dye_" + item[1]["addition"][len("minecraft:"):-len("_dye")]
    return item[1]["addition"]

recipes.sort(key=get_name)

draw = ImageDraw.Draw(template)

index = 0
for recipe in recipes:
    item = recipe[1]["addition"].replace("minecraft:", "")
    name = recipe[0].replace("_", " ").title()
    if item.endswith("carpet"):
        item.replace("_wool_", "_")
    item_img = Image.open(f"img/items/{item}.png").convert("RGBA")

    template.paste(any_wool, (top_left[0] + next_offset[0] * index, top_left[1] + next_offset[1] * index))
    template.paste(item_img, (top_left[0] + right_offset[0] + next_offset[0] * index, top_left[1] + right_offset[1] + next_offset[1] * index))

    draw.text([text_top_left[0] + next_offset[0] * index, text_top_left[1] + next_offset[1] * index], name, font=font)
    
    index += 1


template.show()
