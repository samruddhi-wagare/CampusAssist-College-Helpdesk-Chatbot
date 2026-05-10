import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' # Suppresses the warnings you see in red
import tensorflow as tf

# Limit TensorFlow memory usage
tf.config.set_visible_devices([], 'GPU')

from flask import Flask, render_template, request, jsonify
import nltk
import pickle
import numpy as np
import json
import random
import sqlite3
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model
model = load_model('chatbot_model.h5')
app = Flask(__name__)

# 1. Initialize AI Brain components
lemmatizer = WordNetLemmatizer()
model = load_model('chatbot_model.h5')
intents = json.loads(open('intents.json').read())
data = pickle.load(open("training_data.pkl", "rb"))
words = data['words']
classes = data['labels']

# 2. AI Processing Functions (Copy-pasted from your chat.py)
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w: bag[i] = 1
    return np.array(bag)

def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return [{'intent': classes[r[0]], 'probability': str(r[1])} for r in results]

def get_response(intents_list, intents_json, user_input):
    if not intents_list:
        return "I'm sorry, I don't understand that."
    
    tag = intents_list[0]['intent']
    
    # SQL Database Check
    if tag == "faculty_check":
        conn = sqlite3.connect('campus.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name, status, room FROM faculty")
        rows = cursor.fetchall()
        conn.close()
        for row in rows:
            if row[0].lower() in user_input.lower():
                return f"{row[0]} is currently {row[1]} in {row[2]}."
        return "Here is the faculty status: " + ", ".join([f"{r[0]} ({r[1]})" for r in rows])

    # Standard JSON Responses
    for i in intents_json['intents']:
        if i['tag'] == tag:
            return random.choice(i['responses'])
    return "I'm not sure how to help with that."

# 3. Flask Routes (The Web Bridges)
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["POST"]) 
def chat():
    # Receive data from the Website
    msg = request.json.get("message")
    if not msg:
        return jsonify({"response": "No message received"})
    
    # Process with AI
    ints = predict_class(msg)
    res = get_response(ints, intents, msg)
    
    # Send result back to Website
    return jsonify({"response": res})

if __name__ == "__main__":
    app.run(debug=True)
