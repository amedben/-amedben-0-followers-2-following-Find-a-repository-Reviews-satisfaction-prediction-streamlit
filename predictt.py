import pickle
import streamlit as st
from tensorflow import keras
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
#import tensorflow_hub as hub
#import tensorflow_text as text
import tensorflow as tf
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import pandas as pd
import numpy as np
from datetime import datetime
import csv
import openai
import sklearn

@st.cache_resource(experimental_allow_widgets=True)
def loadmodellstm():
    model=tf.keras.models.load_model('LSTM.h5',compile=False)
    return model

@st.cache_resource(experimental_allow_widgets=True)
def loadmodelgru():
    model=tf.keras.models.load_model('GRU.h5',compile=False)
    return model

@st.cache_resource(experimental_allow_widgets=True)
def loadtk():
    model=pickle.load(open('tokenizer2.pkl','rb'))
    return model

@st.cache_resource(experimental_allow_widgets=True)
def loadcv():
    model=pickle.load(open('CountVectorizer.pkl','rb'))
    return model

@st.cache_resource(experimental_allow_widgets=True)
def loadnb():
    model=pickle.load(open('nb.pkl','rb'))
    return model

bertlstm=loadmodellstm()
bertgru=loadmodelgru()

tokenizer=loadtk()
countvectorizer= loadcv()
nb=loadnb()

nltk.download('stopwords')
nltk.download('wordnet')
def remove_punctuation_numbers(text):
    return re.sub(r'[^a-zA-Z]', ' ', text)


def remove_stopwords(text):
    stop_words = set(stopwords.words('english'))
    stop_words.remove('not')
    words = text.split()
    filtered_words = [word for word in words if word.lower() not in stop_words]
    return ' '.join(filtered_words)


def lemmatize_text(text):
    lemmatizer = WordNetLemmatizer()
    words = text.split()
    lemmatized_words = [lemmatizer.lemmatize(word) for word in words]
    return ' '.join(lemmatized_words)

def preprocess(data):
  data = pd.DataFrame({'text': [data]})
  data['text'] = data['text'].str.lower()
  data['text'] = data['text'].apply(remove_punctuation_numbers)
  data['text']= data['text'].apply(remove_stopwords)
  data['text'] = data['text'].apply(lemmatize_text)
  X = tokenizer.texts_to_sequences(data['text'])
  X = pad_sequences(X, maxlen=59, padding='post')
  X = np.array(X, dtype=np.int32)
  return X

def preprocess2(data):
  data = pd.DataFrame({'text': [data]})
  data['text'] = data['text'].str.lower()
  data['text'] = data['text'].apply(remove_punctuation_numbers)
  data['text']= data['text'].apply(remove_stopwords)
  data['text'] = data['text'].apply(lemmatize_text)
  X=countvectorizer.transform(data['text'])
  return X

def predictgru(text):
    #text = pd.DataFrame({'text': [text]})
    text= preprocess(text)
    predection =bertgru.predict(text)
    return float(predection)

def predictlstm(text):
    #text = pd.DataFrame({'text': [text]})
    text= preprocess(text)
    predection =bertlstm.predict(text)
    return float(predection)

def predictnb(text):
    #text = pd.DataFrame({'text': [text]})
    text= preprocess2(text)
    predection =nb.predict(text)
    print(predection)
    return float(predection)


def addrecord(text,result,correct):
    field_names = ['date', 'review', 'predection','correct']
    date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    record_data = [date, text, result,correct]
    with open('usage_records.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        is_new_file = file.tell() == 0
        if is_new_file:
            writer.writerow(field_names)

        writer.writerow(record_data)


#text1='Absolutely wonderful'
#text2="i don't like this dress it does not look like the picture and did not fit me well"
#res=predict(text1)

#print(res[0][0])
