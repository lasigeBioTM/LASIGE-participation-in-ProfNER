import os
import sys
from flair.data import Corpus
from flair.datasets import ColumnCorpus
from flair.embeddings import FlairEmbeddings, StackedEmbeddings, WordEmbeddings, FastTextEmbeddings
from flair.models import SequenceTagger
from flair.trainers import ModelTrainer
#from pre_process_NER import cantemist_to_IOB2

sys.path.append("./")

## Set the gpus to use
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
#os.environ["CUDA_VISIBLE_DEVICES"] = "0,1,2,3"

## Convert the CANTEMIST corpus into IOB2 format and load it as a ColumnCorpus object 
# see: https://github.com/flairNLP/flair/blob/master/resources/docs/TUTORIAL_6_CORPUS.md


data_folder = './profner/subtask-2/BIO-for-flair/'
columns = {0: 'text', 4: 'ner'}
corpus: Corpus = ColumnCorpus(data_folder, columns,
                              column_delimiter= ' ',
                              train_file='train_final.txt',
                              test_file='valid_spacy.txt'
                              )

print(corpus)
## Train the model
#see: https://github.com/flairNLP/flair/blob/master/resources/docs/TUTORIAL_7_TRAINING_A_MODEL.md

# 2. what tag do we want to predict?
tag_type = 'ner' 

# 3. make the tag dictionary from the corpus
tag_dictionary = corpus.make_tag_dictionary(tag_type=tag_type) 
print(tag_dictionary)

# 4. initialize trained embeddings
ner_model = str(sys.argv[1]) #base, medium
embedding_types = list()


if ner_model == "base":
    embedding_types = [WordEmbeddings('es'), 
                    FlairEmbeddings('es-forward'), 
                    FlairEmbeddings('es-backward')]

elif ner_model == "twitter":
    embedding_types = [FastTextEmbeddings("./uncased/covid_19_es_twitter_cbow_uncased.bin")]

elif ner_model == "medium":
    embedding_types = [WordEmbeddings('es'),
                    FlairEmbeddings('es-forward'), 
                    FlairEmbeddings('es-backward'),
                    FastTextEmbeddings("./uncased/covid_19_es_twitter_cbow_uncased.bin")]
                # or FlairEmbeddings('../embeddings/twitter/pytorch_model.bin')


# List of available embeddings in FLAIR: https://github.com/flairNLP/flair/tree/master/resources/docs/embeddings

embeddings: StackedEmbeddings = StackedEmbeddings(embeddings=embedding_types)

# 5. initialize sequence tagger
tagger: SequenceTagger = SequenceTagger(hidden_size=256,
                                        embeddings=embeddings,
                                        tag_dictionary=tag_dictionary,
                                        tag_type=tag_type,
                                        use_crf=True)

# 6. initialize trainer
trainer: ModelTrainer = ModelTrainer(tagger, corpus)

#If the training ends abruplty without creating the file final-model.pt, load from last checkpoint and continue training:
#from pathlib import Path
#checkpoint = 'resources/taggers/' + ner_model '/checkpoint.pt'
#trainer = ModelTrainer.load_checkpoint(checkpoint, corpus)

# 7. start training
output_dir = './resources/taggers/' + ner_model
trainer.train(output_dir,
              learning_rate=0.1,
              mini_batch_size=32,
              max_epochs=55,
              train_with_dev=True,
              monitor_train=True,
              monitor_test=True,
              checkpoint=True,
              embeddings_storage_mode='none',
              patience=3)




