from passage import *
from query import *
import nltk
import Algorithmia
from nltk.tag import StanfordNERTagger
from nltk import word_tokenize
from utilities import get_subject
import webcolors

# NER = StanfordNERTagger('http://localhost:9000')
def get_colors(text):
    words = word_tokenize(text)
    colrs = []
    for x in words:
        if x.lower() in webcolors.css3_names_to_hex:
            colrs.append(x)
    return colrs

def get_result(entity,ranks,sentences,query):

    client = Algorithmia.client('simR9dr2dF79zdimoXRNAWioLhp1')
    algo = client.algo('StanfordNLP/NamedEntityRecognition/0.2.0')
    algo.set_options(timeout=300) # optional
    
    print("Possible Answers are : ")
    flag = 0
    query_sub = get_subject(query)
    print("Query subject : ",query_sub)
    if "color" in query:
        for x in ranks:
            colors = get_colors(sentences[x])
            if(len(colors)>0):
                output = ' '.join(colors)
                print(output)
                return
    
    for x in ranks:
        # print("sentence subject : ",get_subject(sentences[x]).lower())
        # if(query_sub.lower()!=get_subject(sentences[x]).lower()):
        #     continue
        if(flag==1):
            break
        # print(NER.tag(word_tokenize(sentences[x])))
        results = algo.pipe(sentences[x]).result
        prev = ""
        for ent in results[0]:
            name = ent[0]
            obj = ent[1]
            if obj in entity:
                if prev==obj:
                    print(name,end=" ")
                    prev = obj
                else :
                    if(flag==1):
                        print()
                    print(name,end=" ")
                    prev = obj
                flag = 1

    if flag==0:
        print("Sorry. No Answers Found!!")
    print()
    print()


    print("Required Entity : ")
    t = [print(i) for i in entity]

    


    



