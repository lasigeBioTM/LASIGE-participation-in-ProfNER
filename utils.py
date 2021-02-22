import sys
sys.path.append("./")


def load_dataset_BIO(subset):
    
    dataset_dir = "./profner/subtask-2/BIO/"
    
    if subset == "train":
        filenames = ["train_spacy.txt", "train_key.txt", "train_random.txt", "train_synonym.txt"]

    elif subset == "dev":
        filenames = ["dev_spacy.txt"]
    
    all_docs = list()
    
    for filename in filenames:
        
        with open(dataset_dir + filename, "r") as in_file:
            in_data = in_file.read()
            in_file.close()
            docs = in_data.split("\n\n")
            all_docs.extend(docs)
        
    return all_docs