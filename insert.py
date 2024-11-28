import os
import psycopg2
from models import add_image_to_db

flickr_8k_folder = 'flickr_8k/images'
captions_file = 'flickr_8k/captions.txt'

captions_dict = {}
with open(captions_file, 'r') as f:
    for line in f:
        parts = line.strip().split(',', 1)
        if len(parts) == 2:
            image_name, caption = parts
            image_name = image_name.strip().lower()
            caption = caption.strip()
            if image_name in captions_dict:
                captions_dict[image_name].append(caption)
            else:
                captions_dict[image_name] = [caption]

for image_name in os.listdir(flickr_8k_folder):
    image_path = os.path.join(flickr_8k_folder, image_name)
    image_name_lower = image_name.lower()
    captions = captions_dict.get(image_name_lower, ["No caption available"])
    for caption in captions:
        add_image_to_db(image_name, image_path, caption)
        print(f"Added {image_name} with caption: {caption}")
