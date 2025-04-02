from flask import Flask, request, jsonify
from chat import get_mood_response, get_chat_response
import time
import random

app = Flask(__name__)

@app.route('/user-mood-check', methods=['GET'])
def handle_mood():
    data = request.get_json()
    print(data)
    mood_description = data['mood_description']
    response = get_mood_response(mood_description)

    return jsonify({'recommendation': response})

@app.route('/user-mood-chat', methods=['POST'])
def handle_chat():
    data = request.get_json()
    user_input = data['user_input']
    mood_description = data['mood_description']
    response = get_chat_response(user_input, mood_description)
    return jsonify({'response': response})

if __name__ == '__main__':
    print("Welcome to the AI-Powered Study Assistant API! 🎓")
    app.run(debug=True)
