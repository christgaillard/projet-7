import os
import app.functions
from datetime import datetime
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
    text = request.get_json()
    clean_tweet = app.tweet_transform(text['body'])
    text_lematized = app.text_lematized(app.remove_stopwords(app.tokenize_words(clean_tweet.lower())))
    return jsonify(text_lematized)



if __name__ == '__main__':
   app.run()