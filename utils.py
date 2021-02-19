import sys
sys.path.append("./")


def load_dataset_BIO(subset):
    
    dataset_dir = "./profner/subtask-2/BIO/"
    
    if subset == "train":
        filename = "train_spacy.txt"

    elif subset == "dev":
        filename = "dev_spacy.txt"
    

    with open(dataset_dir + filename, "r") as in_file:
        in_data = in_file.read()
        in_file.close()
        docs = in_data.split("\n\n")

    return docs