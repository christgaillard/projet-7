import re
import nltk

nltk.download('punkt')
nltk.download('stopwords') #import des stopwords anglais.
from nltk.corpus import stopwords

ps = nltk.PorterStemmer()
stop_words = stopwords.words('english')   # on veille à charger les mots correspondants à la langue du document.

'''
Fonction pour le nettoyage du texte
supprime les @, http, nombres etc...
'''
def tweet_transform(tweet):
    '''

    :param tweet: String
    :return: String
    '''
    text = re.sub(r'https?:\/\/.\S+', "", tweet)
    text = re.sub(r'#', '', text)
    text = re.sub(r'@([a-zA-z]*)', '', text)
    text = re.sub(r'^RT[\s]+', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    return text

'''
Découpe les phrases en listes de mots.
'''
def tokenize_words(text):
    '''
    :param text : string
    :return: List[]
    '''
    tokens = re.split('\W+', text)
    return tokens


'''
Supprime les mots récurrants, ayant un faible impacte sur le sens du texte.
'''
def remove_stopwords(texts):
    '''
    :param texts: List[]
    :return: List[]
    '''
    text = [word for word in texts if word not in stop_words]
    return text

'''
Traite chaque mots afin de le maitre à l'indicatif, et au singulier
dans notre cas, fonctionne trés bien avec l'anglais.
'''
def stemming(texts):
    '''

    :param texts: list[]
    :return: list[]
    '''
    text = [ps.stem(word) for word in texts]
    trans_sentence = text

    return trans_sentence
'''
aplique en une fois tout les traitements de textes.
renvois le texte prét pour le modèle
'''
def pipe_text(texts):
    texts = tweet_transform(texts)
    texts = tokenize_words(texts)
    texts = remove_stopwords(texts)
    texts = stemming(texts)
    return texts

