from flask import Flask, render_template, request, jsonify
from transformers import pipeline
import os
import random

app = Flask(__name__)

# Load the sentiment analysis pipeline
sentiment_analysis = pipeline('sentiment-analysis')

# Define keyword lists for custom emotions
happy_keywords = ['happy', 'good mood', 'having a great day', 'joyful', 'excited']
sad_keywords = ['sad', 'low', 'down', 'unhappy', 'depressed']
angry_keywords = ['angry', 'mad', 'furious', 'annoyed', 'irritated']
party_mood_keywords = ['party', 'celebrate', 'celebrating', 'fun', 'festive']

def keyword_based_sentiment(text):
    text_lower = text.lower()

    if any(word in text_lower for word in angry_keywords):
        return 'angry'
    elif any(word in text_lower for word in party_mood_keywords):
        return 'party'
    elif any(word in text_lower for word in happy_keywords):
        return 'happy'
    elif any(word in text_lower for word in sad_keywords):
        return 'sad'
    else:
        return 'unknown'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sentiment', methods=['POST'])
def sentiment():
    data = request.get_json()
    text = data.get('text', '')

    if text:
        # First check for keywords
        keyword_sentiment = keyword_based_sentiment(text)
        if keyword_sentiment != 'unknown':
            sentiment = keyword_sentiment
        else:
            # If no keywords found, use the sentiment analysis model
            result = sentiment_analysis(text)
            label = result[0]['label']
            sentiment = 'happy' if label == 'POSITIVE' else 'sad'

        # Select a random song based on sentiment
        song_path = select_random_song(sentiment)
        return jsonify({'sentiment': sentiment, 'song': song_path})
    return jsonify({'error': 'No text provided'})

def select_random_song(emotion):
    emotion_folder = os.path.join('static', emotion)
    songs = os.listdir(emotion_folder)
    if songs:
        return os.path.join(emotion, random.choice(songs))
    return None

if __name__ == '__main__':
    app.run(debug=True)
