# LASIGE-participation-in-ProfNER

[ProfNER Homepage](https://temu.bsc.es/smm4h-spanish/)

[Schema with the pipeline](https://docs.google.com/presentation/d/1uQNmCLS-81W1j-xsnzrp4NjSLi2iVUu3JFMFtdpmCVU/edit?usp=sharing)

## 1. Data augmentation

To perform data augmentation in train set (train_spacy.txt):

```

python src/mer/data_augmentation.py

```

Output: train_spacy.txt + train_key.txt + train_random.txt + train_synonym.txt in dir "profner/subtask-2/BIO/


## 2. MER

[Python implementation of MER](https://pypi.org/project/merpy/)

### 2.1. To create and process lexicons for MER

- First lexicon: "profession. It includes mentions belonging to "PROFESION" category in train files + synonyms, and entities in profner-gazetteer.tsv + synonyms. Output in "profesion_list.txt"

- Second lexicon: "situacion". It includes mentions belonging to "SITUACION_LABORAL" category in train files. Output in "situacion_laboral_list.txt"


### 2.2. Named Entity Recognition

To recognize entities in test set:

```

python src/mer/mer_annotate.py

```

Output: "valid_task1.txt" and "valid_task2_txt"


## 3. FLAIR tagger

### 3.1. Preprocessing

To prepare train files for FLAIR:

```

python src/flair/flair_pre_process.py 

```

### 3.2. Training

To train a FLAIR tagger:

```

python src/flair/train_ner_model_2.py <model>

```

Arg <model>:
- "base": [Spanish FLAIR embeddings](https://github.com/flairNLP/flair/blob/master/resources/docs/embeddings/FLAIR_EMBEDDINGS.md)
- "twitter": FastText Spanish COVID-19 CBOW uncased. [Download](https://zenodo.org/record/4449930#.YC_gturLdak)
- "medium": Combination of previous embeddings.

Output in "resources/taggers/<model>"

### 3.3. Named Entity Recognition
To recognize entities in test set:

```

python src/flair/predict_ner.py

```

	


