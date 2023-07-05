from flask import Flask, render_template, request, jsonify
import random
import os
from datetime import datetime, timedelta
from termcolor import colored

app = Flask(__name__)

# Constants
WORD_LENGTH = 5
MAX_ATTEMPTS = 6
TIMER_DURATION = 180  # 3 minutes in seconds

# Function to generate a random word
def generate_word():
    word_list = ["stove", "grape", "apple", "honey", "flame", "table", "fence", "lucky", "scent", "novel",
                 "chess", "frost", "wrist", "juice", "waste", "virus", "sweep", "beard", "shaft", "shock",
                 "brick", "beast", "sight", "curse", "treat", "charm", "yield", "frown", "horse", "spoil",
                 "bless", "bonus", "queen", "river", "sweat", "braid", "grasp", "blend", "cliff", "crane",
                 "shelf", "doubt", "rider", "bunch", "nurse", "vital", "tiger", "trick", "wool", "cabin",
                 "flash", "sweep", "grill", "drain", "blame", "sting", "curve", "lemon", "spear", "steak",
                 "wrist", "plaza", "prize", "swamp", "glory", "stool", "angel", "ocean", "black", "stair",
                 "shirt", "chair", "craft", "shade", "steel", "roast", "order", "proud", "thief", "broom"]
    return random.choice(word_list)


# Function to check the correctness of the guess
def check_guess(guess, target_word):
    feedback = []
    for i in range(WORD_LENGTH):
        if guess[i] == target_word[i]:
            feedback.append({'letter': guess[i], 'color': 'green', 'visible': True})  # Correct letter in the correct position
        elif guess[i] in target_word:
            feedback.append({'letter': guess[i], 'color': 'yellow', 'visible': True})  # Correct letter in the wrong position
        else:
            feedback.append({'letter': guess[i], 'color': 'red', 'visible': True})  # Incorrect letter
    return feedback


# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')


# Route for playing the game
@app.route('/play', methods=['POST'])
def play():
    target_word = generate_word()
    attempts = 0
    grid = []
    start_time = datetime.now()
    end_time = start_time + timedelta(seconds=TIMER_DURATION)

    while attempts < MAX_ATTEMPTS and datetime.now() <= end_time:
        elapsed_time = datetime.now() - start_time
        guess = request.form['guess'].lower()

        if len(guess) != WORD_LENGTH:
            return jsonify({'message': 'Invalid guess. Guess should be {} letters long.'.format(WORD_LENGTH)})

        feedback = check_guess(guess, target_word)
        grid.append(feedback)

        if feedback == [{'letter': guess[i], 'color': 'green', 'visible': True} for i in range(WORD_LENGTH)]:
            elapsed_time = datetime.now() - start_time
            return jsonify({
                'message': 'Congratulations! You guessed the word.',
                'grid': grid,
                'elapsed_time': elapsed_time.seconds
            })

        attempts += 1

    elapsed_time = datetime.now() - start_time
    if attempts == MAX_ATTEMPTS:
        return jsonify({
            'message': 'Sorry, you have used all your attempts.',
            'grid': grid,
            'elapsed_time': elapsed_time.seconds
        })
    elif datetime.now() > end_time:
        return jsonify({
            'message': 'Sorry, you ran out of time.',
            'grid': grid,
            'elapsed_time': elapsed_time.seconds
        })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
