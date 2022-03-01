import os
import yaml
import PIL.Image, PIL.ImageFont, PIL.ImageDraw

with open("card_list.yaml") as f:
    card_list = yaml.safe_load(f)

def path(s):
    return os.path.join(*s.split("/"))

field_fonts = {
    field_name: PIL.ImageFont.truetype(path(config["font"]), config["fontSize"])
    for field_name, config in card_list["fields"].items()
}

for card_index, card in enumerate(card_list["cards"]):
    card = {**card_list["defaultConfig"], **card}
    img = PIL.Image.open(path(card["baseImage"]))
    draw = PIL.ImageDraw.Draw(img)
    for field_name, value in card.items():
        if field_name == "baseImage":
            continue
        field_data = card_list["fields"][field_name]
        draw.text(
            (field_data["x"], field_data["y"]),
            str(value),
            tuple(field_data["color"]),
            font=field_fonts[field_name],
        )
    save_path = path(f"outputs/{card_index:03d}-{card['name']}.png")
    print("Saving to:", save_path)
    img.save(save_path)
