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


def write_header(model):
    
    # Output the annotation file
    if ner_model=="medium":
        annotation_filepath = '../evaluation/flair_subtask_2/medium/valid.tsv'  
    elif ner_model=="base":
        annotation_filepath = '../evaluation/flair_subtask_2/base/valid.tsv' 
    elif ner_model=="large":
        annotation_filepath = '../evaluation/flair_subtask_2/large/valid.tsv'

    output = str()
    header = "tweet_id" + "\t" + "begin" + "\t" + "end" + "\t" + "type" + "\t" + "extraction" + "\n"

    with open(annotation_filepath, 'w', encoding='utf-8') as annotation_file:
        annotation_file.write(header)
        #annotation_file.close()
    

def build_annotation_file(doc, doc_filepath, model,filenames):
    

    # Output the annotation file
    if ner_model=="medium":
        annotation_filepath = '../evaluation/flair_subtask_2/medium/valid.tsv'  
    elif ner_model=="base":
        annotation_filepath = '../evaluation/flair_subtask_2/base/valid.tsv' 
    elif ner_model=="large":
        annotation_filepath = '../evaluation/flair_subtask_2/large/valid.tsv'
        
    
    output = str()
    header = "tweet_id" + "\t" + "begin" + "\t" + "end" + "\t" + "type" + "\t" + "extraction" + "\n"


    annotation_file = open(annotation_filepath, 'a', encoding='utf-8')
    
      
    with open(doc_filepath, 'r', encoding='utf-8') as doc_file:
        text = doc_file.read()
        doc_file.close()
    
    # Sentence segmentation followed by tokenization of each sentence
    doc_spacy = nlp(text)
    sent_begin_position = int(0)
    annot_number = int()
    
    for spacy_sent in doc_spacy.sents:
        

        #print(spacy_sent)
        if len(spacy_sent.text) >= 2 and spacy_sent.text[0] == "\n":
            sent_begin_position -= 1


        sentence = Sentence(spacy_sent.text, use_tokenizer=True)
        model.predict(sentence)
            
        for entity in sentence.get_spans('ner'):

            
            if str(entity.tag) == "PROFESION":
                 annot_number += 1
                 begin_entity = str(sent_begin_position+entity.start_pos)
                 end_entity = str(sent_begin_position+entity.end_pos)
                 entity_text = "" 
                 output += str(doc[:-4]) + "\t" + begin_entity + "\t" + end_entity + "\t" + "PROFESION" +  "\t" + str(entity.text) + "\n"
                 filenames.append(doc[:-4])
                 

            elif str(entity.tag) == "SITUACION_LABORAL":
                 annot_number += 1
                 begin_entity = str(sent_begin_position+entity.start_pos)
                 end_entity = str(sent_begin_position+entity.end_pos)
                 entity_text = "" 
                 output += str(doc[:-4]) + "\t" + begin_entity + "\t" + end_entity + "\t" + "SITUACION LABORAL" + "\t" + str(entity.text) + "\n"
                 filenames.append(doc[:-4])
                 

            elif str(entity.tag) == "ACTIVIDAD":
                 annot_number += 1
                 begin_entity = str(sent_begin_position+entity.start_pos)
                 end_entity = str(sent_begin_position+entity.end_pos)
                 entity_text = "" 
                 output += str(doc[:-4]) + "\t" + begin_entity + "\t" + end_entity + "\t" + "ACTIVIDAD" + "\t" + str(entity.text) + "\n"
                 filenames.append(doc[:-4])
                 

            elif str(entity.tag) == 'FIGURATIVA' :
                 annot_number += 1
                 begin_entity = str(sent_begin_position+entity.start_pos)
                 end_entity = str(sent_begin_position+entity.end_pos)
                 entity_text = "" 
                 output += str(doc[:-4]) + "\t" + begin_entity + "\t" + end_entity + "\t" + "FIGURATIVA" + "\t" + str(entity.text) + "\n"
                 filenames.append(doc[:-4])
                 
                
        
            print(output)


        sent_begin_position += len(spacy_sent.text) + 1

        
        
    with open(annotation_filepath, 'a', encoding='utf-8') as annotation_file:
        annotation_file.write(output)
        annotation_file.close()

    if str(doc[:-4]) not in filenames:
        with open(annotation_filepath, 'a', encoding='utf-8') as annotation_file:
            annotation_file.write(str(doc[:-4]) + "\t" + "-" + "\t" + "-" + "\t" + "-" + "\t" + "-" + "\n")
            annotation_file.close()

    
    
            
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


    write_header(model)
    
    filenames = []
    
    for doc in os.listdir(test_dir): #Build a file with the tweet_id and annotation of all the documents
        doc_filepath = test_dir + doc
        write_header(model)
        build_annotation_file(doc, doc_filepath, model, filenames)

    
                
print(build_annotation_file(doc, doc_filepath, model))
