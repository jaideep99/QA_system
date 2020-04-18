from utilities import remove_contractions
from utilities import get_entity,resolve_pronoun
from passage import get_ranked
from entities import get_result,get_aux_result
from nltk import word_tokenize
from utilities import aux_verbs

root = "C:\\Users\\jaide\\OneDrive\\Documents\\VSCODE\\QA_system\\"
text = open("passages\\pass1.txt",'r').read()
queries = open("questions\\ques1.txt",'r').read()


text = remove_contractions(text)
queries = queries.split('\n')
text = resolve_pronoun(text)

for query in queries:
    print("for query : "+query) 
    ranks,sentences = get_ranked(query,text)
    start_word = word_tokenize(query)
    if start_word[0] in aux_verbs:
        get_aux_result(ranks,sentences,query)
    else:
        entity = get_entity(query)
        results = get_result(entity,ranks,sentences,query)
    print()
    print()


