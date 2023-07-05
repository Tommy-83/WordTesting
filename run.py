from flask import Flask, render_template, request
import random
from datetime import datetime, timedelta

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
@app.route('/', methods=['GET', 'POST'])
def play_game():
    if request.method == 'POST':
        guess = request.form['guess'].lower()

        # Validate the guess
        if len(guess) != WORD_LENGTH:
            return render_template('index.html', message='Invalid guess. Guess should be {} letters long.'.format(WORD_LENGTH))

        # Play the game
        target_word = generate_word()
        grid = []
        attempts = 0
        start_time = datetime.now()
        end_time = start_time + timedelta(seconds=TIMER_DURATION)

        while attempts < MAX_ATTEMPTS and datetime.now() <= end_time:
            elapsed_time = datetime.now() - start_time

            feedback = check_guess(guess, target_word)
            grid.append(feedback)

            if feedback == [{'letter': guess[i], 'color': 'green', 'visible': True} for i in range(WORD_LENGTH)]:
                elapsed_time = datetime.now() - start_time
                return render_template('index.html', grid=grid, elapsed_time=elapsed_time, target_word=target_word,
                                       message="Congratulations! You guessed the word.")

            attempts += 1

        elapsed_time = datetime.now() - start_time
        if attempts == MAX_ATTEMPTS:
            return render_template('index.html', grid=grid, elapsed_time=elapsed_time, target_word=target_word,
                                   message="Sorry, you have used all your attempts.")
        elif datetime.now() > end_time:
            return render_template('index.html', grid=grid, elapsed_time=elapsed_time, target_word=target_word,
                                   message="Sorry, you ran out of time.")

    # Render the initial page
    return render_template('index.html')

if __name__ == '__main__':
    app.run()

