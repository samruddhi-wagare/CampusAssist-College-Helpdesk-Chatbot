import sqlite3
import random
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model

# Ensure required resources are available
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()
intents = json.loads(open('intents.json').read())

# Load the saved metadata and the model
data = pickle.load(open("training_data.pkl", "rb"))
words = data['words']
classes = data['labels']
model = load_model('chatbot_model.h5')

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    
    # INCREASE THIS THRESHOLD
    # 0.70 means the bot must be 70% sure before it speaks
    ERROR_THRESHOLD = 0.70 
    
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    results.sort(key=lambda x: x[1], reverse=True)
    
    # If the bot isn't sure, it returns an empty list
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    
    # Fallback logic: if return_list is empty, return a 'no_answer' intent
    if not return_list:
        return_list.append({'intent': 'noanswer', 'probability': '1.0'})
        
    return return_list

def get_response(intents_list, intents_json, user_input): # Ensure 'user_input' is here
    if not intents_list:
        return "I'm sorry, I don't understand that."
    
    tag = intents_list[0]['intent']
    
    # SQL Database Logic
    if tag == "faculty_check":
        import sqlite3 # Import inside the function is fine
        conn = sqlite3.connect('campus.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name, status, room FROM faculty")
        rows = cursor.fetchall()
        conn.close()
        
        # Check if the user mentioned a specific name from our DB
        for row in rows:
            if row[0].lower() in user_input.lower():
                return f"{row[0]} is currently {row[1]} in {row[2]}."
        
        # If no specific name was mentioned, list everyone
        response = "Here is the current faculty status:\n"
        for row in rows:
            response += f"- {row[0]}: {row[1]}\n"
        return response

    # Static JSON Logic
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result

print("GO! CampusAssist is running! (Type 'quit' to stop)")

while True:
    message = input("You: ")
    if message.lower() == "quit":
        break
        
    ints = predict_class(message)
    res = get_response(ints, intents, message) # Added 'message'
    print("Bot:", res)