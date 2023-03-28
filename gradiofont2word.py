import gradio as gr
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageColor
import random
import os

def apply_random_transformations(img):
    # Apply random horizontal flip
    if random.choice([True, False]):
        img = ImageOps.mirror(img)
    # Apply random vertical flip
    if random.choice([True, False]):
        img = ImageOps.flip(img)
    # Apply random rotation
    rotations = [0, 90, 180, 270, 360,0, 90, 180, 270]
    rotation_angle = random.choice(rotations)
    img = img.rotate(rotation_angle, expand=True)
    return img

def export_word_to_png(word, font_name, image_size_height, image_size_width, text_size, output_folder, text_color, bg_color, text_color_influence, flip_text_overlay, text_overlay, bg_color_influence, bg_overlay):
    word = word.replace(" ", "")
    font_name = font_name.name
    # create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    word_folder = f"{output_folder}/{word}"
    if not os.path.exists(word_folder):
        os.makedirs(word_folder)
    # create sorted list of letters in word
    letters = list(word)

    # load font
    font = ImageFont.truetype(font_name, size=text_size)

    images = []
    # create an image for each letter and save it as a PNG
    for i, letter in enumerate(letters):
        # create the background
        if bg_overlay:
            img = Image.open(bg_overlay).resize((int(image_size_width), int(image_size_height))).convert("RGBA")
            img2 = Image.new("RGBA", (image_size_width, image_size_height), bg_color)
            # Set the opacity for each image
            opacity = bg_color_influence / 100
            # Blend the images together based on their opacity
            img = Image.blend(img, img2, opacity)
        else:
            img = Image.new("RGBA", (image_size_width, image_size_height), bg_color)
        draw = ImageDraw.Draw(img)

        # draw the letter in the center of the image
        w, h = draw.textsize(letter, font=font)
        x = (image_size_width - w) / 2
        y = (image_size_height - h) / 2
        draw.text((x, y), letter, font=font, fill=text_color)

        # apply text overlay if specified
        if text_overlay:
            overlay = Image.open(text_overlay).convert("RGBA")
            overlay = overlay.resize((int(image_size_width), int(image_size_height)))
            text_color_2 = Image.new("RGBA", (image_size_width, image_size_height), text_color)
            # Set the opacity for each image
            opacity = text_color_influence / 100
            # Blend the images together based on their opacity
            overlay = Image.blend(overlay, text_color_2, opacity)
            #create a mask from the letter
            if flip_text_overlay:
                overlay = apply_random_transformations(overlay)
            mask = Image.new("L", overlay.size, 0)
            mask_draw = ImageDraw.Draw(mask)
            mask_draw.text((x, y), letter, font=font, fill=255)
            # resize mask to match the size of the image
            mask = mask.resize(img.size)
            # apply alpha mask to the overlay
            overlay.putalpha(mask)
            img = Image.alpha_composite(img, overlay)
            
        # save the image as a PNG in the output folder
        file_name = f"{word_folder}/{i+1:06d}{letter}.png"
        img.save(file_name)
        images.append(file_name)
        #image_paths.append(file_name)
    return f"Images exported successfully. Folder path: {os.path.abspath(word_folder)}", images


font_input = gr.inputs.File(label="Font name", type="file")
word_input = gr.inputs.Textbox(label="Word", default="Hello world!")
image_size_height_input = gr.inputs.Slider(minimum=512, maximum=1024, step=64, label="Image Size h", default=512)
image_size_width_input = gr.inputs.Slider(minimum=512, maximum=1024, step=64, label="Image Size w", default=512)
text_size_input = gr.inputs.Slider(minimum=50, maximum=1024, step=10, label="Text Size", default=350)
output_folder_input = gr.inputs.Textbox(label="Output Folder", default="output")

text_color_input = gr.ColorPicker(label="Text Color", value="#ffffff")
text_influence_input = gr.inputs.Slider(label="Text color Influence on image overlay", minimum=0, maximum=100, default=0)
flip_text_overlay_input = gr.inputs.Checkbox(label="Randomize text image overlay flip and rotation", default=True)
text_overlay_input = gr.Image(label="Text image Overlay", type="filepath")

bg_color_input = gr.ColorPicker(label="Background Color", value="#000000")
bg_influence_input = gr.inputs.Slider(label="background color Influence on background image", minimum=0, maximum=100, default=0)
bg_overlay_input = gr.Image(label="Background image Overlay", type="filepath")


output = gr.outputs.Textbox(label="Output Message")
gallery = gr.Gallery(
            label="Generated images", show_label=False, elem_id="gallery"
        ).style(grid=[2], height="auto")

interface = gr.Interface(fn=export_word_to_png, 
                         inputs=[word_input, font_input, image_size_height_input, image_size_width_input, text_size_input, 
                                 output_folder_input, text_color_input, bg_color_input, text_influence_input, flip_text_overlay_input, text_overlay_input, bg_influence_input, bg_overlay_input], 
                         outputs=[output, gallery], 
                         title="Export Word to PNG Images",
                         description="Enter a word and a font name and this app will export a PNG image for every letter of the word in the chosen font. PNG names will be sorted alphabetically based on the letters in the word.",
                         layout="horizontal", 
                         theme="compact", 
                         defaults={"Font File": "Helvetica-Bold-Font.ttf"})

interface.launch()