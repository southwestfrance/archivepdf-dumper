import requests
import os

API_URL = "https://apdf-strapi-294wm.ondigitalocean.app/scans"
BASE_PDF_URL = "https://apdf.devs-591.workers.dev/file/apdf-strapi-media-library"

# false if you just want the links
DOWNLOAD = True 
OUTPUT_DIR = "pdfs"

os.makedirs(OUTPUT_DIR, exist_ok=True)

res = requests.get(API_URL)
data = res.json()

links = []

for entry in data:
    pdf = entry.get("pdf")
    if not pdf:
        continue
    
    hash_ = pdf.get("hash")
    if not hash_:
        continue
    
    url = f"{BASE_PDF_URL}/{hash_}.pdf"
    links.append(url)

    if DOWNLOAD:
        filename = os.path.join(OUTPUT_DIR, f"{hash_}.pdf")
        print("Downloading:", filename)
        r = requests.get(url)
        with open(filename, "wb") as f:
            f.write(r.content)

# save list of links
with open("links.txt", "w") as f:
    for l in links:
        f.write(l + "\n")

print("Done. Total PDFs:", len(links))
