import sys
sys.path.append('../util')
import data_io
import json
import numpy as np
import csv
import scipy
from tqdm import tqdm

wordfile = '../data/glove.42B.300d.txt' # word vector file, can be downloaded from GloVe website
weightfile = '../data/enwiki_vocab_min200.txt' # each line is a word and its frequency (needs downloads)
weightpara = 1e-3 # the parameter in the SIF weighting scheme, usually in the range [3e-5, 3e-3]

# load word vectors
(words, We) = data_io.getWordmap(wordfile)
# load word weights
word2weight = data_io.getWordWeight(weightfile, weightpara) # word2weight['str'] is the weight for the word 'str'
weight4ind = data_io.getWeight(words, word2weight) # weight4ind[i] is the weight for the i-th word

documents = json.loads(open('../data/document.txt', 'r', encoding='utf-8').read())

# n = words['satti']
# print(len(We[n]))
# print(weight4ind[n])

def encode(sentence):
    import string
    sentence = sentence.lower().translate(str.maketrans('', '', string.punctuation)).split()

    return np.mean([We[words[w]] * weight4ind[words[w]] for w in sentence if w in words], axis=0)

dV = []
for d in documents:
    vector = encode(d)
    dV.append(vector)
# for d in dV:
#     for c in dV:
#         print(scipy.spatial.distance.cosine(c, d))


path = '../data/'
rows = list(csv.reader(open(path+'companies2WithMissions.csv', 'r',encoding='utf-8',newline='')))[1:]
wr = csv.writer(open(path+'evaluation.csv', 'w',encoding='utf-8',newline=''))
wr.writerow(['Organization', 'Mission', 'Families', 'Educators', 'Workspace'])

for r in tqdm(rows):
    name, msg = r[0], r[-1]
    v = encode(msg)
    similarities = [scipy.spatial.distance.cosine(v, dv) for dv in dV]
    wr.writerow([name] + similarities)

