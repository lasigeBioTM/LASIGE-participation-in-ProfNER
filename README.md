# LASIGE-participation-in-ProfNER

[ProfNER Homepage](https://temu.bsc.es/smm4h-spanish/)

[Schema with the pipeline](https://docs.google.com/presentation/d/1uQNmCLS-81W1j-xsnzrp4NjSLi2iVUu3JFMFtdpmCVU/edit?usp=sharing)

## 1. Data augmentation
original train file (train_spacy.txt) + train files with augmented data (train_key.txt, train_random.txt, train_synonym.txt) in dir "profner/subtask-2/BIO/

## 2. MER

[Python implementation of MER](https://pypi.org/project/merpy/)

Mentions belonging to "PROFESION" category:
- profner-gazetteer.tsv 
- synonyms of profner-gazetteer.tsv 
- trainning set (4 versions)

Mentions belonging to "SITUACION_LABORAL" category
- trainning set (4 versions)

## 3. FLAIR tagger

### Embeddings
- FastText Spanish COVID-19 CBOW uncased. Download [here](https://zenodo.org/record/4449930#.YC_gturLdak)
- Spanish Flair embeddings. See [tutorial](https://github.com/flairNLP/flair/blob/master/resources/docs/embeddings/FLAIR_EMBEDDINGS.md)
