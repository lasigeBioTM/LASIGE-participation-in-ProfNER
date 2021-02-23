import os
import sys

ner_model = str(sys.argv[1])


if not os.path.exists("./evaluation/flair_subtask_1/"):
    os.makedirs("./evaluation/flair_subtask_1/")
if not os.path.exists("./evaluation/flair_subtask_1/medium"):
    os.makedirs("./evaluation/flair_subtask_1/medium")
if not os.path.exists("./evaluation/flair_subtask_1/base"):
    os.makedirs("./evaluation/flair_subtask_1/base")
if not os.path.exists("./evaluation/flair_subtask_1/large"):
    os.makedirs("./evaluation/flair_subtask_1/large")




task2File = './evaluation/flair_subtask_2/' + ner_model + '/valid.tsv'

out = './evaluation/flair_subtask_1/' + ner_model + '/valid.tsv'

header = "tweet_id" + "\t" + "label" + "\n"

with open(out, 'w',encoding = 'utf-8') as outFile:
    outFile.write(header)
    


with open(task2File,'r',encoding = 'utf-8') as inFile:
    inlines = inFile.readlines()
    for i in inlines[1:] :
        ids = i.split("\t")
        if ids[1] == '-':
            outLine = str(ids[0]) + "\t" + "0" + "\n"
        else :
            outLine = str(ids[0]) + "\t" + "1" + "\n"


        with open(out, 'a',encoding = 'utf-8') as outFile:
            outFile.write(outLine)
            outFile.close()
                
