import os
import pickle
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
    request_data = request.get_json()
    text = request_data[0]['body']
    request_data[0]['body']= wp.stemming(wp.remove_stopwords(wp.tokenize_words(wp.tweet_transform(text))))
    return jsonify(request_data)





if __name__ == '__main__':
   app.run()