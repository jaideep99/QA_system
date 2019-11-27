from passage import *
from query import *
import nltk
import Algorithmia
from pycorenlp import StanfordCoreNLP
from nltk import word_tokenize
from utilities import get_subject,get_subjects
import webcolors

nlp = StanfordCoreNLP('http://localhost:9000')


def get_colors(text):
    words = word_tokenize(text)
    colrs = []
    for x in words:
        if x.lower() in webcolors.css3_names_to_hex:
            colrs.append(x)
    return colrs

def check_sent(text):
    res = nlp.annotate(text,
                   properties={
                       'annotators': 'sentiment',
                       'outputFormat': 'json',
                       'timeout': 1000,
                   })
    for s in res["sentences"]:

        if s["sentiment"]=='Positive' or s["sentiment"]=='Neutral':
            return 1
        else:
            return -1

def get_result(entity,ranks,sentences,query):

    client = Algorithmia.client('simR9dr2dF79zdimoXRNAWioLhp1')
    algo = client.algo('StanfordNLP/NamedEntityRecognition/0.2.0')
    algo.set_options(timeout=300) # optional
    
    print("Possible Answers are : ")
    flag = 0
    query_sub = get_subject(query)
    if "color" in query:
        for x in ranks:
            colors = get_colors(sentences[x])
            if(len(colors)>0):
                output = ' '.join(colors)
                print(output)
                return
    
    for x in ranks:
        if(flag==1):
            print()
            print(sentences[ranks[0]])
            print()
            break

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
        # print("Sorry. No Answers Found!!")
        # print("Next possible answers : ")
        print(sentences[ranks[0]])



def get_aux_result(ranks,sentences,query):

    sentence = sentences[ranks[0]]
    
    sen = check_sent(sentence)
    que = check_sent(query)

    sen_subs = get_subjects(sentence)
    que_subs = get_subjects(query)

    flag = 0
    for x in que_subs:
        if x not in sen_subs:
            print(x)
            flag=1
            break

    

    if sen*que<0:
        print("No!!")
    else :
        if flag==0:
            print("Yes!!")
        else:
            print("No!!")




    


    



