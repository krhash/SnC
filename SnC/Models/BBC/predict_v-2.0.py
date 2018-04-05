import pickle
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from keras.models import load_model,model_from_json
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import model_from_json
import numpy as np
import time
import os
from sys import argv

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
dir_path = os.path.dirname(os.path.realpath(__file__))
categories = ['business','entertainment','politics','sport','tech']
max_doc_length = 1500
to_predict = ""

a = time.time()

def getopts(argv):
    opts = {}  # Empty dictionary to store key-value pairs.
    while argv:  # While there are arguments left to parse...
        if argv[0][0] == '-':  # Found a "-name value" pair.
            opts[argv[0]] = argv[1]  # Add key and value to the dictionary.
        argv = argv[1:]  # Reduce the argument list by copying it starting from index 1.
    return opts
    
def preprocess():
    stop_words = set(stopwords.words('english'))
    tokenizer_r = RegexpTokenizer(r'[a-z]+')

    with open(dir_path + '/tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)
        tokenizer.oov_token = None

    data = list()

    with open(to_predict,'r') as f:
         doc = f.read()
         tokens = tokenizer_r.tokenize(doc.lower())
         doc = " ".join(list(filter(lambda x: x not in stop_words,tokens)))

    doc_files = list()
    doc_files.append(doc)

    documents = tokenizer.texts_to_sequences(doc_files)
    data = pad_sequences(documents, maxlen=max_doc_length,padding='post')

    return data[0]

def load_trained_model():

    with open(dir_path + '/model.json','r') as f:
        loaded_model = f.read()

    model = model_from_json(loaded_model)
    model.load_weights(dir_path + '/model.h5')

    return model

def predict():

    model = load_trained_model()

    pr_data = np.zeros((1,max_doc_length))
    pr_data[0] = preprocess()

    p=model.predict(np.array(pr_data))
    #print(p)
    print(categories[np.argmax(p[0])])
    #p[0][np.argmax(p[0])] = 0
    #print(categories[np.argmax(p[0])])
    #print("time:"+str(time.time()-a))

myargs = getopts(argv)
to_predict = myargs["-f"]
predict()
