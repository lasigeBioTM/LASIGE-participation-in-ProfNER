import csv
import merpy
import nlpaug.augmenter.word as naw
import os
import sys
sys.path.insert(0,'./src/')
from utils import load_dataset_BIO

sys.path.append("./")


def find_entities_of_interest(docs, category):

    entities = list()
    synonym_word = naw.SynonymAug(aug_src='wordnet', lang='spa')
    
    for doc in docs:

        if doc != "":    
            tokens = doc.split("\n")
            entity = str()
            previous_token = str()
                
            for token in tokens:
                info = token.split(" ")
                
                token_category = info[4][2:] 
             
                if info[4][0] == "B" and token_category == category:
                    
                    if previous_token == "I" or previous_token == "B" and token_category == previous_category:
                        entities.append(entity)
                   
                    entity = str()
                    entity += info[0].lower()
                    previous_token = "B"
                    previous_category = token_category

                elif info[4][0] == "I" and token_category == category:
                    entity += " " + info[0].lower()
                    previous_token = "I"
                    previous_category = token_category
                        
                elif info[4][0] == "O":

                    if previous_token == "I" or previous_token == "B":
                        entities.append(entity)
                   
                    previous_category = str() 
                    previous_token = "O"
        
    return entities
    

def process_dicts_4_mer(category):

    train_docs = load_dataset_BIO("train")
    all_docs = train_docs
    #dev_docs = load_dataset_BIO("dev") #uncomment only in Evaluation phase, to make predictions on test set
    #all_docs = train_docs + dev_docs 
    synonym_word = naw.SynonymAug(aug_src='wordnet', lang='spa')
    entities = list()

    if category == "PROFESION" or category == "PROFESION_short": # 1. Retrieve mentions in the several files of train set
        entities = find_entities_of_interest(all_docs, "PROFESION")
        print("Professions (PROFESSION) retrieved from train files!")
    
        if category == "PROFESION_short": #2. retrieves entities in gazeteer
            filepath = "occupations-gazetteer/profner-gazetteer.tsv"

            with open(filepath) as gazetter_file:
                reader = csv.reader(gazetter_file, delimiter="\t")
                row_count = int()
                
                for row in reader:
                    row_count += 1
                    
                    if row_count > 2:
                        entities.append(row[0])
                        entities.append(row[1])
                    
                        synonym_1 = synonym_word.augment(row[1])

                        if synonym_1 != row[1]:
                            entities.append(synonym_1)
        
        print("Professions (PROFESSION) retrieved from the gazetter!")
        
    elif category == "SITUACION_LABORAL" or category == "ACTIVIDAD" or category == "FIGURATIVA":
        #3. retrieves mentions from train set
        entities = find_entities_of_interest(all_docs, category)
        print(category + " mentions retrieved from train files")
    
    output_filepath = category.lower() + "_list.txt"
    output = str()

    for entity in entities:

        if entity not in entities_unique:
            output += entity + "\n"
            entities_unique.append(entity)

    with open(output_filepath, "w") as out_file:  
        out_file.write(output)
        out_file.close()


def create_lexicons():

    categories = ["PROFESION", "PROFESION_short" "SITUACION_LABORAL", "ACTIVIDAD", "FIGURATIVA"]
    
    for category in categories:
        process_dicts_4_mer(category)

    with open("profesion_list.txt", "r") as professions_file:
        data = professions_file.read()
        professions = [entity for entity in data.split("\n")]
        professions_file.close()
    
    with open("profesion_short_list.txt", "r") as professions_short_file:
        data = professions_short_file.read()
        professions_short = [entity for entity in data.split("\n")]
        professions_short_file.close()
    
    with open("situacion_laboral_list.txt", "r") as situacion_file:
        data = situacion_file.read()
        situacion_laboral = [entity for entity in data.split("\n")]
        situacion_file.close()

    with open("actividad_list.txt", "r") as actividad_file:
        data = actividad_file.read()
        actividad = [entity for entity in data.split("\n")]
        actividad_file.close()

    with open("figurativa_list.txt", "r") as figurativa_file:
        data = figurativa_file.read()
        figurativa = [entity for entity in data.split("\n")]
        figurativa_file.close()
    
    merpy.create_lexicon(professions, "profesion")
    merpy.create_lexicon(professions_short, "profesionShort")
    merpy.create_lexicon(situacion_laboral, "situacion")
    merpy.create_lexicon(actividad, "actividad")
    merpy.create_lexicon(figurativa, "figurativa")
    
    merpy.process_lexicon("profesion")
    merpy.process_lexicon("profesionShort")
    merpy.process_lexicon("situacion")
    merpy.process_lexicon("actividad")
    merpy.process_lexicon("figurativa")
   
    print(merpy.show_lexicons())


def generate_output_file():

    test_dir = "profner/txt-files/valid/" #Change in Evaluation phase to "profner/txt-files/test/"
    docs_with_entities = list()
    output_entities = list()
    test_count = int()
    
    for test_file in os.listdir(test_dir):
        test_count+=1
        
        with open(test_dir + test_file, "r") as in_file:
            text = in_file.read()
            in_file.close()

        doc_id = test_file.strip(".txt")
        
        professions = merpy.get_entities(text, "profesionShort")
        working_status = merpy.get_entities(text, "situacion")
        actividad = merpy.get_entities(text, "actividad")
        figurativa = merpy.get_entities(text, "figurativa")
        
        if professions[0] != ['']: 

            if (doc_id, "1") not in docs_with_entities:
                docs_with_entities.append((doc_id, "1"))
                
            for profession in professions:
                
                output_entities.append((doc_id, profession[0], profession[1], "PROFESION", profession[2]))

        if working_status[0] != ['']:
            
            if (doc_id, "1") not in docs_with_entities: 
                docs_with_entities.append((doc_id, "1"))

            for work in working_status:
                
                if work[2].lower() != "sin":
                    print(work)
                    output_entities.append((doc_id, work[0], work[1], "SITUACION_LABORAL", work[2]))
        
        if actividad[0] != ['']:
            
            if (doc_id, "1") not in docs_with_entities: 
                docs_with_entities.append((doc_id, "1"))

            for act in actividad:
                output_entities.append((doc_id, act[0], act[1], "ACTIVIDAD", act[2]))
                
        if figurativa[0] != ['']:
            
            if (doc_id, "1") not in docs_with_entities: 
                docs_with_entities.append((doc_id, "1"))

            for fig in figurativa:
                output_entities.append((doc_id, fig[0], fig[1], "FIGURATIVA", fig[2]))
        
        if working_status[0] == [''] and professions[0] == [''] and actividad[0] == [''] and figurativa[0] == [''] : 
            output_entities.append((doc_id, "-", "-", "-", "-"))
            docs_with_entities.append((doc_id, "0"))

    #Task 1 output file
    with open('valid_task1.tsv', 'w', newline='') as out_file1:
        tsv_writer = csv.writer(out_file1, delimiter='\t',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        
        header = ["tweet_id", "label"]
        tsv_writer.writerow(header)

        for entity in docs_with_entities:
            tsv_writer.writerow(entity)

    #Task 2 output file
    with open('valid_task2.tsv', 'w', newline='') as out_file2:
        tsv_writer = csv.writer(out_file2, delimiter='\t',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        
        header = ["tweet_id", "begin", "end", "type", "extraction"]
        tsv_writer.writerow(header)

        for entity in output_entities:
            tsv_writer.writerow(entity)


if __name__ == "__main__": 
    lexicons = sys.argv[1]

    if lexicons: #In the first run it is necessary to create and process the lexicons for MER
        create_lexicons()

    else:
        generate_output_file()

