# Datathon - Finding Potential Partners for Understood.org with NLP

finalEvaluation shows the fitness of organizations, in terms of the mission of Understood.org and specific focus in families, educator and workspace. Smaller value means better fits. The last column Rank is the combination of the previous 4 columns (0.5 * Mission + 0.5 * (Families + Educators + Workspace) / 3)

## Mechanisms
To find the potential partneers, I compare the discriptions of the missions from Understood with the mission statement of other organizations using NLP. More specifically, I encode every word of a sentence to a vectore through GloVe, adding smaller weights to insignificant words words so they don't direct the sentence vector much. Finally, I compare the vectors encoded from organizations with those from Understood by Cosine distance.

## Codes
- grabDoc: spider through Understood.org
- getOrgs: get nonprofit organizations' information on guidestar.org
- evaluate: use WordEmbedding + Smooth Inverse Frequency + Consine Lost to compare paragraphs from organizations and understood.org

## Data
- document: texts on webpages from Understood.org
- companies: informations of nonprofit organizations from guidestar.org
- evaluation: comparison result (smaller values means better fit)

## Util
- utility codes from [Github Repo](https://github.com/PrincetonML/SIF)
- data_io: utility tools to process files


## Reference 
@article{arora2017asimple, 
	author = {Sanjeev Arora and Yingyu Liang and Tengyu Ma}, 
	title = {A Simple but Tough-to-Beat Baseline for Sentence Embeddings}, 
	booktitle = {International Conference on Learning Representations},
	year = {2017}
}