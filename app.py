import os
import pickle
import numpy as np
from keras.saving.save import load_model
from keras.utils import pad_sequences

import webapp.functions as wp #import des fonctions
from flask import Flask, render_template, request, redirect, url_for, send_from_directory,jsonify


app = Flask(__name__) #initialisation de Flask

# page d'accueil de l'app
@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


# definition du point d'entrée de l'appWeb
@app.route('/tweet', methods=['POST'])

def tweet():
    response_data=[]
    mondict= {}
    with open(os.path.join(app.root_path, 'tokenizer_glove'), 'rb') as handle :
        tokenizer = pickle.load(handle) # chargement du Tokenizer pré entrainé
    model = load_model(os.path.join(app.root_path, 'my_model_Glove_LSTM')) # chargement du modèle pre entrainé
    request_data = request.get_json() # recupération des données envoyées en POST
    text = request_data[0]['body'] # recupération du texte
    rs_text = wp.pipe_text(text) # traitement du texte
    k_sequence_len = 41 # definition de la longueur de séquence, doit correspondre au longueurs utilisées pour l'entrainement.
    #créer notre séquence à partir du texte du tweet
    x_val = pad_sequences(tokenizer.texts_to_sequences([rs_text]),
                                                        maxlen= k_sequence_len,
                                                        padding='post')

    y_pred_proba = model.predict(x_val) #prediction de notre tweet
    y_pred = np.where(y_pred_proba > 0.5, 1, 0)
    if y_pred[0][0] == 1 :
        sent = "Ce tweet est positif"
    else:
        sent = "Ce tweet est négatif"

    mondict['pred'] = sent
    mondict['proba'] =  str(y_pred_proba[0][0])
    response_data.append(mondict) # renvoit de la réponse
    print(response_data)
    return jsonify(response_data)





if __name__ == '__main__':
   app.run()