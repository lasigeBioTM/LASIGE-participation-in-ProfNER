# LASIGE-participation-in-ProfNER

The track [ProfNER-ST: Identification of professions \& occupations in Health-related Social Media"](https://temu.bsc.es/smm4h-spanish/) in the context of the [\#SMM4H 2021](https://healthlanguageprocessing.org/smm4h-shared-task-2021/) included two different sub-tracks:

- Track A: Tweet binary classification
- Track B: NER offset detection and classification

This repository contains the code associated with the participation of the Lasige-BioTM team in both sub-tracks of ProfNER.

[Draft schema with the pipeline](https://docs.google.com/presentation/d/1uQNmCLS-81W1j-xsnzrp4NjSLi2iVUu3JFMFtdpmCVU/edit?usp=sharing)

-------------------------------------------------------------------------------------------------------------------
## 1. Setup

### 1.1. Data

To get the necessary data (ProfNER corpus, occupations gazeteer, ...) execute the following script:

```

./get_data.sh

```

### 1.2. Requirements

To install the necessary requirements execute the following script:

```

pip install -r requirements.txt

```

-------------------------------------------------------------------------------------------------------------------

## 2. Preprocessing

To perform **data augmentation** in the train set (train_spacy.txt) using [nlpaug](https://github.com/makcedward/nlpaug) library

```

python src/data_augmentation.py

```

Output: train_spacy.txt + train_key.txt + train_random.txt + train_synonym.txt in dir "profner/subtask-2/BIO/

-------------------------------------------------------------------------------------------------------------------

## 3. MER

[Python implementation of MER](https://pypi.org/project/merpy/)

### 3.1. To create and process lexicons for MER

The following lexicons are created and processed for MER: 

- 1st lexicon "profesionShort": it includes mentions belonging to "PROFESION" category in train files + synonyms (output in "profesion_list.txt")

- 2nd lexicon "profesion": mentions belonging to "PROFESION" category in train files + synonyms, and entities in profner-gazetteer.tsv + synonyms 

- 3rd lexicon "situacion": mentions belonging to "SITUACION_LABORAL" category in train files (output in "situacion_laboral_list.txt")

- 4th lexicon "actividad": mentions belonging to "ACTIVIDAD" category in train files (output in "actividad_list.txt")

- 5th lexicon "figurativa": mentions belonging to "FIGURATIVA" category in train files (output in "figurativa_list.txt")

Run the script:

```

python src/mer/mer_annotate.py <mode>

```

Arg:
- <mode>: if it is the first run, has value "lexicon", otherwise has value "predict"

### 3.2. Tweet classification and Named Entity Recognition

To recognize entities in test set, classify tweets, and generate predictions file for both sub-tracks run the same script with a different value for the first argument:

```

python src/mer/mer_annotate.py predict

```

Output: "valid_task1.txt" and "valid_task2_txt" with predictions for sub-track 7a and 7b, respectively.

-------------------------------------------------------------------------------------------------------------------

## 4. FLAIR tagger

[FLAIR](https://github.com/flairNLP/flair) framework

### 4.1. Preprocessing

To prepare train files for FLAIR:

```

python src/flair/flair_pre_process.py 

```

### 4.2. Training

To train the NER tagger:

```

python src/flair/train_ner_model.py <model>

```

Arg <model>:
- "base": [Spanish FLAIR embeddings](https://github.com/flairNLP/flair/blob/master/resources/docs/embeddings/FLAIR_EMBEDDINGS.md)
- "twitter": FastText Spanish COVID-19 CBOW uncased. [Download](https://zenodo.org/record/4449930#.YC_gturLdak)
- "medium": Combination of previous embeddings.

Output in "resources/taggers/<model>"

### 4.3. Prediction
To recognize entities in test set and generate the output file:

```

python src/flair/predict_ner.py <model>

```

Arg <model>:
- "base": [Spanish FLAIR embeddings](https://github.com/flairNLP/flair/blob/master/resources/docs/embeddings/FLAIR_EMBEDDINGS.md)
- "twitter": FastText Spanish COVID-19 CBOW uncased. [Download](https://zenodo.org/record/4449930#.YC_gturLdak)
- "medium": Combination of previous embeddings.

Output TSV file in "/evaluation/flair_subtask_2/<model>"
	
### 3.4. Tweet classification
To determine if a tweet in test set contains a mention of occupation:

```
python src/flair/flair_classification_tweet.py <model>

```
Arg <model>:
- "base": [Spanish FLAIR embeddings](https://github.com/flairNLP/flair/blob/master/resources/docs/embeddings/FLAIR_EMBEDDINGS.md)
- "twitter": FastText Spanish COVID-19 CBOW uncased. [Download](https://zenodo.org/record/4449930#.YC_gturLdak)
- "medium": Combination of previous embeddings.

Output TSV file in "/evaluation/flair_subtask_1/<model>"


	

