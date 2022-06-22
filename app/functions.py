import re
import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords

ps = nltk.PorterStemmer()


def tweet_transform(tweet):
    text = re.sub(r'https?:\/\/.\S+', "", tweet)
    text = re.sub(r'#', '', text)
    text = re.sub(r'@([a-zA-z]*)', '', text)
    text = re.sub(r'^RT[\s]+', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    return text


def tokenize_words(text):
    tokens = re.split('\W+', text)
    return tokens


stop_words = stopwords.words('english')   # on veille à charger les mots correspondants à la langue du document.


def remove_stopwords(texts):
    text = [word for word in texts if word not in stop_words]
    return text


def stemming(tokenized_text):
    text = [ps.stem(word) for word in tokenized_text]
    trans_sentence = ' '.join(text)
    return trans_sentence
