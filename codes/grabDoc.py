import requests
from lxml import etree
import re

def getTexts():
    url = ['https://www.understood.org/about/our-mission',
    'https://www.understood.org/pages/en/families', 
    'https://www.understood.org/pages/en/school-learning/for-educators',
    # 'https://www.understood.org/pages/en/young-adults/',
    'https://www.understood.org/pages/en/workplace/']

    def cleanse(text):
        text = text.replace('\n', '').strip()
        text = re.sub(' +', ' ', text)
        return text
        

    dataset = []

    for i in url:
        res = requests.get(i)
        tree = etree.HTML(res.text)
        texts = tree.xpath("//main//text()")
        texts = [cleanse(str(t)) for t in texts]
        texts = [t for t in texts if t is not '']
        dataset.append(' '.join(texts))

    return dataset

if __name__ == "__main__":
    t = getTexts()
    import json
    open('document.txt', 'w', encoding='utf-8').write(json.dumps(t))
    
    # print(t[0])
    print(t)