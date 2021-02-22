import os
import sys
sys.path.append("./")

bio_dir = "./profner/subtask-2/BIO/"
out_dir = "./profner/subtask-2/BIO-for-flair/"

# delete characters that are not readable by python
for doc in os.listdir(bio_dir):
    outFile = open(out_dir + doc, 'w', encoding='utf-8')
    with open(bio_dir + doc,'r',encoding='utf-8') as files:
        lines = files.readlines()
        #print(lines)
        for i in lines:
            if not i.startswith(('"','️')):
                outFile.write(i)
        outFile.close()



#merge the train files in one
files = [out_dir + "train_key.txt", out_dir + "train_random.txt", out_dir + "train_synonym.txt", out_dir + "train_spacy.txt"]

outFile = open(out_dir + "train_final.txt","w", encoding = 'utf-8')

for file in files:
    with open(file, encoding = 'utf-8') as infile:
        outFile.write(infile.read())
    outFile.write("\n")
    #outFile.close()
    
        
        
