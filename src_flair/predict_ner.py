import os 
import sys
from flair.data import Sentence
from flair.models import SequenceTagger
from flair.embeddings import FlairEmbeddings
from flair.data import Sentence
import spacy
from spacy.lang.es import Spanish
from spacy.pipeline import SentenceSegmenter

os.environ['CUDA_LAUNCH_BLOCKING'] = '1'

sys.path.append("./")

ner_model=str(sys.argv[1])

def build_annotation_file(doc, doc_filepath, model):

    output = str()

    with open(doc_filepath, 'r', encoding='utf-8') as doc_file:
        text = doc_file.read()
        doc_file.close()
    
    # Sentence segmentation followed by tokenization of each sentence
    doc_spacy = nlp(text)
    #print(text)
    #print(str(doc))
    #print(doc_spacy)
    sent_begin_position = int(0)
    annot_number = int()
    for spacy_sent in doc_spacy.sents:

        #print(spacy_sent)
        if len(spacy_sent.text) >= 2 and spacy_sent.text[0] == "\n":
            sent_begin_position -= 1
        #if len(spacy_sent.text) > 512:
            #spacy_sent = spacy_sent[:512]

        sentence = Sentence(spacy_sent.text, use_tokenizer=True)
        model.predict(sentence)
        #print(type(sentence))
            
        for entity in sentence.get_spans('ner'):
            
            if str(entity.tag).strip("\n") == "B-PROFESION":
                 annot_number += 1
                 begin_entity = str(sent_begin_position+entity.start_pos)
                 end_entity = str(sent_begin_position+entity.end_pos)
                 entity_text = "" 
                 #output += "T" + str(annot_number) + "\t" + "PROFESION" + " " + begin_entity + " " + end_entity + "\t" + str(entity.text) + "\n"
                 output += str(doc[:-3]) + "\t" + begin_entity + "\t" + end_entity + "\t" + "PROFESION" +  + str(entity.text) + "\n"

            elif str(entity.tag).strip("\n") == "B-SITUACION_LABORAL":
                 annot_number += 1
                 begin_entity = str(sent_begin_position+entity.start_pos)
                 end_entity = str(sent_begin_position+entity.end_pos)
                 entity_text = "" 
                 #output += "T" + str(annot_number) + "\t" + "SITUACION LABORAL" + " " + begin_entity + " " + end_entity + "\t" + str(entity.text) + "\n"
                 output += str(doc[:-3]) + "\t" + begin_entity + "\t" + end_entity + "\t" + "SITUACION LABORAL" +  + str(entity.text) + "\n"


        sent_begin_position += len(spacy_sent.text) + 1
        #else:
           #del sentence 
    #print(l)
    # Output the annotation file
    if ner_model=="medium":
        annotation_filepath = '../evaluation/flair_subtask_2/medium/' + doc[:-3] + 'ann'
    elif ner_model=="base":
        annotation_filepath = '../evaluation/flair_subtask_2/base/' + doc[:-3] + 'ann'
    elif ner_model=="large":
        annotation_filepath = '../evaluation/flair_subtask_2/large/' + doc[:-3] + 'ann'


    #print(l)
    print(annotation_filepath)
    
        

    with open(annotation_filepath, 'w', encoding='utf-8') as annotation_file:
        annotation_file.write(output)
        annotation_file.close()
        #print(l)
            


#print(l)
if __name__ == "__main__":
    # load the model you trained
    if ner_model=="medium":
        model = SequenceTagger.load('../resources/taggers/medium/final-model.pt')
    elif ner_model=="base":
        model = SequenceTagger.load('../resources/taggers/base/final-model.pt')
    elif ner_model=="large":
        model = SequenceTagger.load('../resources/taggers/large/final-model.pt')






    
    ## Create spanish sentence segmenter with Spacy
    # the sentence segmentation by spacy is non-destructive, i.e., the empty lines are considered when getting a span of a given word/entity
    nlp = Spanish()
    sentencizer = nlp.create_pipe("sentencizer")
    nlp.add_pipe(sentencizer)
    
    test_dir = "../profner/txt-files/valid/"
    
    
    if not os.path.exists("../evaluation/flair_subtask_2/"):
        os.makedirs("../evaluation/flair_subtask_2/")
    if not os.path.exists("../evaluation/flair_subtask_2/medium"):
        os.makedirs("../evaluation/flair_subtask_2/medium")
    if not os.path.exists("../evaluation/flair_subtask_2/base"):
        os.makedirs("../evaluation/flair_subtask_2/base")
    if not os.path.exists("../evaluation/flair_subtask_2/large"):
        os.makedirs("../evaluation/flair_subtask_2/large")




    #corpus._test = [x for x in corpus.test if len(x) <= 384]

    for doc in os.listdir(test_dir): #For each document in test_dir build the respective annotation file with predicted entities
        doc_filepath = test_dir + doc
        build_annotation_file(doc, doc_filepath, model)

                
print(build_annotation_file(doc, doc_filepath, model))
