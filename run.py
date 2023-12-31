from flask import Flask, render_template, request
import random
from jinja2 import Environment

app = Flask(__name__)

words = [
    "apple", "beach", "camel", "dance", "eagle",  # Add more words here...
]

attempts = 0
guessed_words = []

env = Environment()
env.globals.update(enumerate=enumerate)

@app.route('/')
def index():
    return render_template('index.html', attempts=attempts, guessed_words=guessed_words, target_word=target_word)


@app.route('/check_word', methods=['POST'])
def check_word():
    global attempts
    global target_word
    word = request.form['word'].lower()
    attempts += 1
    response = {'missed': 0, 'wrong_placed': 0, 'correct': 0}

    if len(word) != 5:
        return "Please enter a 5-letter word."

    for i, char in enumerate(word):
        if char in target_word:
            if char == target_word[i]:
                response['correct'] += 1
            else:
                response['wrong_placed'] += 1
        else:
            response['missed'] += 1

    guessed_words.append((word, response))
    return render_template('index.html', attempts=attempts, guessed_words=guessed_words, target_word=target_word)


if __name__ == '__main__':
    target_word = random.choice(words)
    app.run(debug=True)
