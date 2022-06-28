import re
import nltk
from keras.layers import Bidirectional
from tensorflow.python.keras import Sequential
from tensorflow.python.keras.layers import Embedding, LSTM, GlobalAveragePooling1D, Dense, Dropout

nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords

ps = nltk.PorterStemmer()
stop_words = stopwords.words('english')   # on veille à charger les mots correspondants à la langue du document.


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



def remove_stopwords(texts):
    text = [word for word in texts if word not in stop_words]
    return text


def stemming(tokenized_text):
    text = [ps.stem(word) for word in tokenized_text]
    trans_sentence = ' '.join(text)
    return trans_sentence


def preprocess_text_fct(tweets_raw) :
    print(tweets_raw.values[0:10])
    print(tweets_raw.shape)
    tweet_train, tweet_test, y_train, y_test = train_test_split(tweets_raw.values, y,
                                                                test_size=0.2, stratify=y,
                                                                random_state=7)
    return tweet_train, tweet_test, y_train, y_test

def build_model_fct() :
    print("Build Keras model ...")

    dropout_level = 0.2

    k_model = Sequential()
    k_model.add(Embedding(vocab_size,
                        w2v_size,
                        weights=[embedding_matrix],
                        input_length=k_max_sequence_len,
                        trainable=True))

    k_model.add(Bidirectional(LSTM(128, dropout=0.5, recurrent_dropout=0.2, return_sequences=True)))
#    k_model.add(TimeDistributed(Dense(256, activation='relu')))
#    k_model.add(Flatten())
    k_model.add(GlobalAveragePooling1D())
    k_model.add(Dense(32, activation='relu'))
    k_model.add(Dropout(dropout_level))
    k_model.add(Dense(1, activation='sigmoid'))

    k_model.compile(loss='binary_crossentropy',
                                optimizer='adam',
                                metrics=['accuracy'])


    return k_model