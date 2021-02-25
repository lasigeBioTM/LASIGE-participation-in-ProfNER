import os
import sys

ner_model = str(sys.argv[1])


if not os.path.exists("./evaluation/flair_subtask_1/"):
    os.makedirs("./evaluation/flair_subtask_1/")
if not os.path.exists("./evaluation/flair_subtask_1/medium"):
    os.makedirs("./evaluation/flair_subtask_1/medium")
if not os.path.exists("./evaluation/flair_subtask_1/base"):
    os.makedirs("./evaluation/flair_subtask_1/base")
if not os.path.exists("./evaluation/flair_subtask_1/twitter"):
    os.makedirs("./evaluation/flair_subtask_1/twitter")




task2File = './evaluation/flair_subtask_2/' + ner_model + '/valid.tsv'

out = './evaluation/flair_subtask_1/' + ner_model + '/valid.tsv'

header = "tweet_id" + "\t" + "label" + "\n"

with open(out, 'w',encoding = 'utf-8') as outFile:
    outFile.write(header)
    


with open(task2File,'r',encoding = 'utf-8') as inFile:
    inlines = inFile.readlines()
    for i in inlines[1:] :
        predict = 0
        ids = i.split("\t")
        if ids[1] == '-':
            outLine = str(ids[0]) + "\t" + "0" + "\n"
            
        else :
            outLine = str(ids[0]) + "\t" + "1" + "\n"
            

        uniquelines = set()
        with open(out, 'r+',encoding = 'utf-8') as outFile:
            l = outFile.readlines()
            if outLine not in l: # to remove duplicates
                outFile.write(outLine)
                uniquelines.add(outLine)
                outFile.close()
                
