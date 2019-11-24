from utilities import remove_contractions
from utilities import get_entity,resolve_pronoun
from passage import get_ranked
from entities import get_result


root = "C:\\Users\\jaide\\OneDrive\\Documents\\VSCODE\\QA_system\\"
text = open(root+"pass1.txt",'r').read()
queries = open(root+"passq.txt",'r').read()


text = remove_contractions(text)
queries = queries.split('\n')
text = resolve_pronoun(text)
print(text)

for query in queries:
    print("for query : "+query) 
    entity = get_entity(query)
    ranks,sentences = get_ranked(query,text)
    results = get_result(entity,ranks,sentences,query)


