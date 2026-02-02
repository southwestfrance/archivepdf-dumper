import requests
import os
import re

length = 0

API_URL = "https://apdf-strapi-294wm.ondigitalocean.app/archives" 
BASE_PDF_URL = "https://apdf-strapi-media-library.s3.us-east-005.backblazeb2.com"

DOWNLOAD = True 
OUTPUT_DIR = "archives"

os.makedirs(OUTPUT_DIR, exist_ok=True)

res = requests.get(API_URL)
data = res.json()

links = []

# function to sanitize folder/filenames
def sanitize(s):
    return re.sub(r'[<>:"/\\|?*]', '_', s)

if DOWNLOAD:
    print("Download: ON")
else:
    print("Download: OFF")

for entry in data:
    title = entry.get("title")
    if not title:
        continue
    else:
        links.append(title)
    
    if DOWNLOAD:
        folder_name = sanitize(title)
        folder_path = os.path.join(OUTPUT_DIR, folder_name)
        os.makedirs(folder_path, exist_ok=True)
    
    media = entry.get("media")
    if not media:
        continue
    
    for entry in media:
        name = entry.get('name')
        url = entry.get('url')
        links.append(url)
        length += 1
        
        if DOWNLOAD:
            safe_name = sanitize(name)
            filename = os.path.join(folder_path, safe_name)
            print("Downloading:", filename)
            r = requests.get(url)
            with open(filename, "wb") as f:
                f.write(r.content)

# save list of links
with open("archive_links.txt", "w") as f:
    for l in links:
        f.write(l + "\n")

print("Done. Total images:", length)
