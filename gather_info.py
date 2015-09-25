import requests
import json
from pprint import pprint
from BeautifulSoup import BeautifulSoup

def extract_text(link):
    r = requests.get(link)
    raw = r.text.encode('utf-8')
    html = BeautifulSoup(raw)
    return html.find('body').text

with open('links') as data_file:    
    links = json.load(data_file)



texts = map(extract_text, links)
print json.dumps(texts)

