# 🎓 CampusAssist AI: Intelligent University Helpdesk

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![AI/ML](https://img.shields.io/badge/AI-Deep%20Learning-orange.svg)](https://www.tensorflow.org/)
[![NLP](https://img.shields.io/badge/NLP-Natural%20Language%20Processing-blueviolet.svg)](https://www.nltk.org/)
[![Web](https://img.shields.io/badge/Framework-Flask-lightgrey.svg)](https://flask.palletsprojects.com/)

**CampusAssist AI** is an end-to-end AI solution designed for **DYP-ATU Talsande**. It leverages **Natural Language Processing (NLP)** and **Deep Learning** to automate university information access and provide real-time faculty status monitoring through a seamless web interface.

---

## 🌟 Key Features
*   **🧠 Advanced NLP Core:** Implements tokenization, lemmatization, and Bag-of-Words (BoW) models to interpret complex student queries.
*   **🤖 Deep Learning Intent Engine:** Built with a Sequential Neural Network (Keras) to classify user intents with high accuracy.
*   **📍 Live Faculty Monitoring:** Integrated with a SQLite database to track real-time faculty status and room occupancy for improved campus management.
*   **📂 Multi-Project Synergy:** Incorporates design principles from previous IoT and AI-based monitoring systems.
*   **☁️ Cloud Ready:** Optimized for deployment on **Render** with a production-grade Gunicorn server.

---

## 🛠️ Technical Stack
*   **Language:** Python 🐍
*   **NLP Library:** NLTK (Natural Language Toolkit) 📚
*   **AI Framework:** TensorFlow & Keras 🧠
*   **Web Framework:** Flask 🧪
*   **Database:** SQLite3 🗄️
*   **Deployment:** Render & Gunicorn 🚀

---

## 🏗️ Project Architecture
```text
CampusAssist/
├── app.py              # Flask server & NLP processing logic
├── chatbot_model.h5    # Trained Sequential Neural Network model
├── intents.json        # Intent Knowledge Base (100+ Tags)
├── campus.db           # SQLite database for faculty status
├── training_data.pkl   # Serialized pre-processed NLP data
├── static/             # Frontend assets (CSS, Images)
└── templates/          # Responsive HTML interface
