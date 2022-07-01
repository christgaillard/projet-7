import os
import pickle

import gensim
import numpy as np
from keras.saving.save import load_model
from keras.utils import pad_sequences
from keras_preprocessing.text import Tokenizer

import webapp.functions as wp
from flask import Flask, render_template, request, redirect, url_for, send_from_directory,jsonify


app = Flask(__name__)


@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/hello', methods=['POST'])
def hello():
   tweet = request.form.get('tweet')

   if tweet:
       print('Request for hello page received with name=%s' % tweet)
       return render_template('hello.html', tweet = tweet)
   else:
       print('Request for hello page received with no name or blank name -- redirecting')
       return redirect(url_for('index'))

@app.route('/tweet', methods=['POST'])

def tweet():
    response_data=[]
    mondict= {}
    with open(os.path.join(app.root_path, 'tokenizer_glove'), 'rb') as handle :
        tokenizer = pickle.load(handle)
    model = load_model(os.path.join(app.root_path, 'my_model_Glove_LSTM'))
    request_data = request.get_json()
    text = request_data[0]['body']
    rs_text = wp.pipe_text(text)
    print(rs_text)
    #prep_text = [gensim.utils.simple_preprocess(text) for text in rs_text]

    k_sequence_len = 41
    x_val = pad_sequences(tokenizer.texts_to_sequences([rs_text]),
                                                        maxlen= k_sequence_len,
                                                        padding='post')

    y_pred_proba = model.predict(x_val)
    y_pred = np.where(y_pred_proba > 0.5, 1, 0)
    #print(y_pred[0][0])
    if y_pred[0][0] == 1 :
        sent = "Ce tweet est positif"
    else:
        sent = "Ce tweet est négatif"

    mondict['pred'] = sent
    mondict['proba'] =  str(y_pred_proba[0][0])
    print(mondict)
    response_data.append(mondict)
    print(response_data)
    return jsonify(response_data)





if __name__ == '__main__':
   app.run()