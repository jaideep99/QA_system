from utilities import remove_contractions
import string
from nltk.stem import WordNetLemmatizer
from nltk import word_tokenize,pos_tag
from nltk.corpus import wordnet

lemmatizer = WordNetLemmatizer()


def make_sentences(passage_text):
    sentences = []
    for x in passage_text.split('. '):
        if len(x)>0:
            x = x.translate(str.maketrans('', '', string.punctuation))
            sentences.append(x)
    return sentences

def get_wordnet_pos(word):
    tag = pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}

    return tag_dict.get(tag, wordnet.NOUN)

def jaccardi_score(mod):

    mat = {}

    for i in range(len(mod)):
        words = set()
        for wrd in word_tokenize(mod[i]):
            wrd = lemmatizer.lemmatize(wrd,pos=get_wordnet_pos(wrd))
            words.add(wrd)

        mat[i] = words
    
    query = mat[len(mat)-1]
    mat.pop(len(mat)-1)
    
    for x in mat:

        score = float(len(mat[x].intersection(query)))/len(mat[x].union(query))
        # print(str(x)+" : ")
        # print(mat[x].intersection(query))
        score = score*100
        mat[x] = score

    print(mat)
    for x in list(mat):
        if(mat[x]==0.0):
            mat.pop(x)
    order = sorted(mat.items(), key=lambda k: k[1])
    order = [x for x,y in order]
    order.reverse()
    print(order)
    return order



def get_ranked(query,text):
    query = remove_contractions(query)
    query = query.translate(str.maketrans('', '', string.punctuation))
    mod = make_sentences(text)
    mod.append(query)
    
    ranks= jaccardi_score(mod)
    return ranks,mod[:-1]



    

