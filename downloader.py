import os
from tqdm import tqdm
from bs4 import BeautifulSoup
import requests
import uuid
import argparse
import time


parser = argparse.ArgumentParser(description='Download image for given search word!')
parser.add_argument('-s','--search',type=str,required=True,help='Enter the search word')
args = parser.parse_args()

search_word = args.search
url = f'https://unsplash.com/s/photos/{search_word}'
res = requests.get(url)

soup = BeautifulSoup(res.text, 'html.parser')


img_links = list()
for link in soup.find_all('img'):
    if link.get('src').startswith('https://images.unsplash.com/photo'):
        img_links.append(link.get('src'))

download_path = os.path.join(os.getcwd(),'images',search_word)
if not os.path.exists(download_path):
    os.makedirs(download_path)

for img_link in tqdm(img_links,desc=f'Downloading image for {search_word}'):
    img = requests.get(img_link)
    time.sleep(.1)
    
    img_name = str(uuid.uuid4())+'.jpg'
    full_path = os.path.join(download_path,img_name)
    
    with open(full_path,'wb') as f:
        f.write(img.content)
