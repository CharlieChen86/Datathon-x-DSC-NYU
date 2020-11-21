import requests
import csv
import os
from tqdm import tqdm
from lxml import etree


url_org = 'https://www.guidestar.org/profile/{}'

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
}

wr = csv.writer(open('companies2WithMissions.csv', 'w', encoding='utf-8', newline=''))
wr.writerow(['Name', 'IrsSubsection', 'Location', 'Ein', 'Mission'])

def getMission(ein):
        
    res = requests.get(url_org.format(ein), headers = headers)
    while res.status_code != 200:
        print(url_org.format(ein))
        print('Error while requesting org page')
        res = requests.get(url_org.format(ein), headers = headers)

    tree = etree.HTML(res.text)

    
    mission = tree.xpath('//p[@id="mission-statement"]/text()')[0].lower()

    return mission


for f in sorted(os.listdir('files'), key=len):
    f = 'files/' + f
    rows = list(csv.reader(open(f, 'r', encoding='utf-8')))

    print(f)
    toWrite = []
    for r in tqdm(rows):
        if len(r) < 5:
            mission = getMission(r[3])
            r.append(mission)
        toWrite.append(r)
    
    wr.writerows(toWrite)
    
