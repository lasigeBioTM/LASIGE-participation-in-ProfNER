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
    #all_docs = train_docs + dev_docs
    synonym_word = naw.SynonymAug(aug_src='wordnet', lang='spa')

    if category == "PROFESION":
        # 1. Retrieve professions in the several files of train set
        profesions = find_entities_of_interest(all_docs, "PROFESION")
        professions_train_count =  len(profesions)
        print("Professions (PROFESSION) retrieved from train files!")
        """
        #2. retrieves entities in gazeteer
        filepath = "occupations-gazetteer/profner-gazetteer.tsv"

        with open(filepath) as gazetter_file:
            reader = csv.reader(gazetter_file, delimiter="\t")
            row_count = int()
            
            for row in reader:
                row_count += 1
                
                if row_count > 2:
                    profesions.append(row[0])
                    profesions.append(row[1])
                
                    synonym_1 = synonym_word.augment(row[1])

                    if synonym_1 != row[1]:
                        profesions.append(synonym_1)
        
        print("Professions (PROFESSION) retrieved from the gazetter!")
        """
    elif category == "SITUACION_LABORAL":
        #3. retrieves working status in train set
        situacion_laboral = find_entities_of_interest(all_docs, "SITUACION_LABORAL")
        print("Working status (SITUACION_LABORAL) retrieved from train files")
        
    output_filepath = category.lower() + "_list.txt"
    output = str()

    if category == "PROFESION":
        profesion_unique = list()

        for profesion in profesions:
            
            if profesion not in profesion_unique:
                output += profesion + "\n"
                profesion_unique.append(profesion)
                
    elif category == "SITUACION_LABORAL":
        situacion_unique = list()

        for situacion in situacion_laboral:

            if situacion not in situacion_unique:
                output += situacion + "\n"
                situacion_unique.append(situacion)

    with open(output_filepath, "w") as out_file:  
        out_file.write(output)
        out_file.close()

process_dicts_4_mer("PROFESION")

def create_lexicons():

    process_dicts_4_mer("PROFESION")
    #process_dicts_4_mer("SITUACION_LABORAL")

    professions = list()

    with open("profesion_list.txt", "r") as professions_file:
        data = professions_file.read()
        professions = [entity for entity in data.split("\n")]
        professions_file.close()
    
    with open("situacion_laboral_list.txt", "r") as situacion_file:
        data = situacion_file.read()
        situacion_laboral = [entity for entity in data.split("\n")]
        situacion_file.close()
    
    merpy.create_lexicon(professions, "profesionShort")
    #merpy.create_lexicon(situacion_laboral, "situacion")
    merpy.process_lexicon("profesionShort")
    #merpy.process_lexicon("situacion")
    
    #merpy.delete_lexicon("profesion")
    print(merpy.show_lexicons())

#create_lexicons()

def generate_output_file():

    test_dir = "profner/txt-files/valid/"
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
        
        if professions[0] != ['']: 

            if (doc_id, "1") not in docs_with_entities:
                docs_with_entities.append((doc_id, "1"))
                
            for profession in professions:
                
                output_entities.append((doc_id, profession[0], profession[1], "PROFESION", profession[2]))

        if working_status[0] != ['']:
            
            if (doc_id, "1") not in docs_with_entities: 
                docs_with_entities.append((doc_id, "1"))

            for work in working_status:
                output_entities.append((doc_id, work[0], work[1], "SITUACION_LABORAL", work[2]))
                
        if working_status[0] == [''] and professions[0] == ['']: 
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


generate_output_file()

