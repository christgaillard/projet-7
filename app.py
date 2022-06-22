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

@app.route('/api/tweet/', methods=['POST'])
def traitement():
    text = request.form.get('tweet')
    dictionnaire = {
        'tweet' : text,
        'valeurs' : [24, 24, 25, 26, 27, 28],
        'unite' : "degrés Celcius"
    }
    if text :
        print('Request for hello page received with name=%s' % text)
        return jsonify(dictionnaire)
        #return render_template('hello.html', tweet=text)
    else :
        print('Request for hello page received with no name or blank name -- redirecting')
        return redirect(url_for('index'))

if __name__ == '__main__':
   app.run()