import os
from PIL import Image
import concurrent.futures
from tqdm import tqdm

def convert_webp_to_jpg(webp_path, jpg_path):
    try:
        with Image.open(webp_path) as image:
            image.save(jpg_path, 'JPEG')

        os.remove(webp_path)
    except IOError:
        pass

def convert_webp_files(directory):
    webp_files = []
    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.webp'):
                webp_path = os.path.join(root, filename)
                jpg_path = os.path.join(root, filename.replace('.webp', '.jpg'))
                webp_files.append((webp_path, jpg_path))

    with tqdm(total=len(webp_files), desc="Converting files") as pbar:
        def convert_file(webp_jpg_paths):
            webp_path, jpg_path = webp_jpg_paths
            convert_webp_to_jpg(webp_path, jpg_path)
            pbar.update(1)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(convert_file, webp_files)

current_dir = os.getcwd()

convert_webp_files(current_dir)