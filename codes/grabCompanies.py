import requests
import json
from lxml import etree
import csv
from tqdm import tqdm
import time

url = 'https://projects.propublica.org/nonprofits/api/v2/search.json?state%5Bid%5D={}&page={}'
url2 = 'https://projects.propublica.org/nonprofits/search?page={}&q=&state%5Bid%5D={}'
org_api_url = 'https://projects.propublica.org/nonprofits/api/v2/organizations/{}.json'
star_url = 'https://www.guidestar.org/profile/{}'

states = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']

wr = csv.writer(open('companies.csv', 'w', encoding='utf-8',newline=''))
wr.writerow(['Name', 'State', 'Address', 'Mission'])

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
}

def visitOrg(ein):

    res = requests.get(org_api_url.format(ein))
    while res.status_code != 200:
        print(org_api_url.format(ein))
        print('Error while requesting org api')
        time.sleep(5)
        res = requests.get(org_api_url.format(ein))
    
    res = res.json()['organization']

    revenue = res['revenue_amount']

    if revenue is None or revenue == 0:
        return


    name = res['name']
    address = res['address']
    state = res['state']

    einE = str(ein)
    einE = (9 - len(einE)) * '0' + einE
    res = requests.get(star_url.format(einE[:2] + '-' + einE[2:]), headers = headers)
    while res.status_code != 200:
        print(star_url.format(einE[:2] + '-' + einE[2:]))
        print('Error while requesting org page')
        time.sleep(5)
        res = requests.get(star_url.format(einE[:2] + '-' + einE[2:]), headers = headers)

    tree = etree.HTML(res.text)

    mission = tree.xpath('//p[@id="mission-statement"]/text()')[0].lower()


    wr.writerow([name, state, address, mission])


for s in states: 

    print(s)
    
    res = requests.get(url.format(s, 0)).json()
    num_pages = res['num_pages']
    print('num_pages', num_pages)

    for p in tqdm(range(num_pages)):
        res = requests.get(url.format(s, p))
        while res.status_code != 200:
            print(url.format(s, p))
            print('Error while requesting page api')
            time.sleep(5)
            res = requests.get(url.format(s, p))
            
        res = res.json()

        org = res['organizations']

        ein = [o['ein'] for o in org]
        
        
        for e in ein:
            visitOrg(e)

            # break

        # res = requests.get(url2.format(p, s), headers = headers)
        # while res.status_code != 200:
        #     print(url2.format(p, s))
        #     print('Error while requesting page web')
        #     time.sleep(0.1)
        #     res = requests.get(url2.format(p, s), headers = headers)

        # tree = etree.HTML(res.text)
        # table = tree.xpath('//table[@id="search-results"]/tbody')
        # loc = '/tr[{}]/td[{}]/text()'

        # row = len(table[0].xpath('/tr'))
        # print('row', row)

        # for r in range(row):
        #     print(table.xpath(loc.format(r, 3)))
        #     exit(0)
