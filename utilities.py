import re
from pycorenlp import StanfordCoreNLP
from nltk import pos_tag,word_tokenize
from nltk.parse.stanford import StanfordDependencyParser
from nltk.parse.corenlp import CoreNLPDependencyParser


parser = CoreNLPDependencyParser('http://localhost:9000')
nlp = StanfordCoreNLP('http://localhost:9000')

# res, = parser.raw_parse("Tom is 20 years old")
# print(res)

entityMap = {'Who': ['PERSON'],'Whom':['PERSON'],'When':['DATE','TIME'],'Which':['LOCATION','ORGANIZATION','DATE'],'Where':['LOCATION','ORGANIZATION'],'How much':['QUANTITY','DURATION','DATE','NUMBER','MONEY'],'How many':['QUANTITY','DURATION','DATE','NUMBER','MONEY'],'What':['QUANTITY','LOCATION','DATE','PERSON','DURATION','NUMBER','MONEY','TIME']}

aux_verbs = ['Can','Could','Is','Did','Do','Does','Will','Would','May','Have','Are','Am','Shall']

def remove_contractions(text):
    text = re.sub('n\'t',' not',text)
    text = re.sub('let\'s','let us',text)
    text = re.sub('\'s',' is',text)
    text = re.sub('\'d',' would',text)
    text = re.sub('\'ll',' will shall',text)
    text = re.sub('\'m',' am',text)
    text = re.sub('\'ve',' have',text)
    text = re.sub('shan\'t','should not',text)
    return text


def get_entity(query):
    for entity in entityMap:
        if entity in query:
            return entityMap[entity]



def resolve(corenlp_output):
    for coref in corenlp_output['corefs']:
        mentions = corenlp_output['corefs'][coref]
        antecedent = mentions[0]  # the antecedent is the first mention in the coreference chain
        for j in range(1, len(mentions)):
            mention = mentions[j]
            if mention['type'] == 'PRONOMINAL':
                # get the attributes of the target mention in the corresponding sentence
                target_sentence = mention['sentNum']
                target_token = mention['startIndex'] - 1
                # transfer the antecedent's word form to the appropriate token in the sentence
                corenlp_output['sentences'][target_sentence - 1]['tokens'][target_token]['word'] = antecedent['text']


def get_resolved_text(corenlp_output):
    """ Print the "resolved" output """
    output = ""
    possessives = ['hers', 'his', 'their', 'theirs']
    for sentence in corenlp_output['sentences']:
        for token in sentence['tokens']:
            output_word = token['word']
            # check lemmas as well as tags for possessive pronouns in case of tagging errors
            if token['lemma'] in possessives or token['pos'] == 'PRP$':
                output_word += "'s"  # add the possessive morpheme
            output_word += token['after']
            output += output_word+' '
    return output

def get_subject(text):
    res, = parser.raw_parse(text)

    res = list(res.triples())
    subject = ""
    for x in res:
        for i in range(len(x)):
            # print(x[i])
            if x[i]=='nsubj':
                subject = x[i+1][0]
                return subject

    for x in res:
        for i in range(len(x)):
            # print(x[i])
            if x[i]=='nmod':
                subject = x[i+1][0]
                return subject

    return subject

def get_subjects(text):
    res, = parser.raw_parse(text)
    res = list(res.triples())
    subject = []
    for x in res:
        for i in range(len(x)):
            # print(x[i])
            if x[i]=='nsubj':
                subject.append(x[i+1][0])

    for x in res:
        for i in range(len(x)):
            if x[i]=='nmod':
                subject.append(x[i+1][0])

    return subject


def resolve_collectives(text):
    
    texts = text.split('. ')

    for i in range(len(texts)):
        replace = ""
        nouns = []
        for pron in ['their','Their','them','Them','They','they']:
            if pron in word_tokenize(texts[i]):
                # print(texts[i])
                stats = 0
                flag = 0
                for prev in range(i-1,-1,-1):

                    if(stats==2 or flag==1 ):
                        break

                    subject = get_subject(texts[prev])
                    pos= pos_tag([subject])
                    # print(pos)
                    pos = pos[0][1]
                    if(pos=='NNS' or pos=='NNPS'):
                            replace = subject
                            flag=1
                            break

                    if(pos=='NN' or pos=='NNP'):
                            if subject not in nouns:
                                nouns.append(subject)
                                stats+=1
                
        if(replace==""):
            replace = ' and '.join(nouns)
        for pron in ['their','Their','them','Them','They','they']:
            texts[i] = texts[i].replace(pron,replace)

    text = '. '.join(texts) 
    return text
    
    

def resolve_pronoun(text):

    output = nlp.annotate(text, properties= {'annotators':'dcoref','outputFormat':'json','ner.useSUTime':'false'})
    resolve(output)
    text = get_resolved_text(output)
    text = resolve_collectives(text)

    return text