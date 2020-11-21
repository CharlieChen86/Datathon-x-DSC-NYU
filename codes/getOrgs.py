import requests
from lxml import etree
import csv
from tqdm import tqdm
import sys


url = 'https://www.guidestar.org/search/SubmitSearch'


headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
}

state = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']

data = {
        'CurrentPage': '1',
        'SearchType': 'org',
        'Sort': 'UNI_revenueTotal'
        }
wr = csv.writer(open('companies2.csv', 'w', encoding='utf-8', newline=''))
wr.writerow(['Name', 'IrsSubsection', 'Location', 'Ein'])



for s in state:

    print(s)
    data['state'] = s

    data['CurrentPage'] = 1

    res = requests.post(url, headers = headers, data = data)

    if res.status_code != 200:
        raise Exception('error when req')
    res = res.json()
    org, total, num = res['Hits'], res['TotalHits'], res['NumHits']

    if num * 10 < total:
        pages = 10
    else:
        print('unexpected')
        print(num, total)
        pages = total // num

    for p in tqdm(range(1, pages + 1)):
        data['CurrentPage'] = p
        res = requests.post(url, headers = headers, data = data)
        if res.status_code != 200:
            raise Exception('error when req')
        res = res.json()

        orgs = res['Hits']

        for o in orgs:

            name = o['OrgName']
            Ein = o['Ein']
            
            IrsSubsection = o['IrsSubsection']
            loc = o['City'] + ', ' + o['State']

            wr.writerow([name, IrsSubsection, loc, Ein])


