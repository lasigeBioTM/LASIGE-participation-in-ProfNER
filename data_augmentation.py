import nlpaug.augmenter.char as nac
import nlpaug.augmenter.word as naw
import nlpaug.augmenter.sentence as nas
import nlpaug.flow as nafc
import nltk
import sys
from nlpaug.util import Action
from utils import load_dataset_BIO
#nltk.download('omw')
sys.path.append("./")


def output_file(output, name):

    dataset_dir = "./profner/subtask-2/BIO/"

    with open(dataset_dir + name, "w") as out_file:
        out_file.write(output)
        out_file.close()


def augment_data(docs, subset):
    """ nlpaug library, see https://github.com/makcedward/nlpaug  """

    #swap_char = nac.RandomCharAug(action="swap")
    key_char = nac.KeyboardAug()
    random_char = nac.RandomCharAug(action="substitute")
    synonym_word = naw.SynonymAug(aug_src='wordnet', lang='spa')

    output_1 = str() 
    output_2 = str()
    output_3 = str()
        
    for doc in docs:

        if doc != "":    
            tokens = doc.split("\n")
            token_dict = dict()
            doc_id = str()
            doc_1 = str()
            doc_2 = str()
            doc_3 = str()
                
            for token in tokens:
                info = token.split(" ")
                doc_id = str(info[1])
                
                if info[4] != "O": 
                    augmented_token_1 = key_char.augment(info[0]) 
                    doc_1 += augmented_token_1 + " " + info[1] + " " + info[2] + " " + info[3] + " " + info[4] + "\n"
                    augmented_token_2 = random_char.augment(info[0])
                    doc_2 += augmented_token_2 + " " + info[1] + " " + info[2] + " " + info[3] + " " + info[4] + "\n"
                    augmented_token_3 = (synonym_word.augment(info[0]))
                    doc_3 += augmented_token_3 + " " + info[1] + " " + info[2] + " " + info[3] + " " + info[4] + "\n"
                    
                else:  
                    token_O = info[0] + " " + info[1] + " " + info[2] + " " +  info[3] + " " +  info[4] + "\n"
                    doc_1 += token_O
                    doc_2 += token_O
                    doc_3 += token_O
                    
        output_1 += doc_1 + "\n"
        output_2 += doc_2 + "\n"
        output_3 += doc_3 + "\n"

    filename_1 = subset + "_key.txt"
    output_file(output_1, filename_1)
    filename_2 = subset + "_random.txt"
    output_file(output_2, filename_2)
    filename_3 = subset + "_synonym.txt"
    output_file(output_3, filename_3)
            
        
augment_data(load_dataset_BIO("train"), "train")
