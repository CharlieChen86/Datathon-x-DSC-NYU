import requests
import csv
from tqdm import tqdm
import time
from lxml import etree
from multiprocessing import Process


# wr.writerow(['Name', 'IrsSubsection', 'Location', 'Ein', 'Mission'])
rows = list(csv.reader(open('companies2.csv', 'r')))[1:]

def helper(start, end):
    url_org = 'https://www.guidestar.org/profile/{}'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
    }

    def getMission(ein):
        
        res = requests.get(url_org.format(ein), headers = headers)
        if res.status_code != 200:
            raise Exception('Error while requesting org page')

        tree = etree.HTML(res.text)

        
        mission = tree.xpath('//p[@id="mission-statement"]/text()')[0].lower()

        return mission

    wr = csv.writer(open('./files/companiesWithMission_{}-{}.csv'.format(start, end), 'w', encoding='utf-8', newline=''))
    rows = list(csv.reader(open('companies2.csv', 'r')))[start: end]

    toWrite = [] 
    for row in tqdm(rows):
        ein = row[3]
        try:
            mission = getMission(ein)
            toWrite.append(row + [mission])
        except:
            open('tomend.txt', 'a',encoding='utf-8').write(str(ein) + '\n')
            toWrite.append(row)
            print(ein)

    wr.writerows(toWrite)


def main():
    i = 1

    print(len(rows))

    STEP = 1000
    processs = []
    while i + STEP <= len(rows):
        processs.append(Process(target=helper, args=(i, i + STEP, )))
        # _thread.start_new_thread(helper, (rows[i: i + STEP], ))
        i += STEP

    processs.append(Process(target=helper, args=(i, i + STEP, )))

    for p in processs:
        p.start()
    print("something")

if __name__ == "__main__":
    main()

