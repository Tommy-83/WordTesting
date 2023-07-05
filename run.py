from flask import Flask, render_template, request
import random
import time
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


# Function to display the game grid
def display_grid(grid, elapsed_time, reveal_word):
    print("    " + " ".join(colored(chr(65+i), 'white') for i in range(WORD_LENGTH)))
    print("  +" + "---+" * WORD_LENGTH)

    for row in grid:
        colored_row = []
        for letter in row:
            if letter['visible']:
                colored_row.append(colored(letter['letter'], letter['color'], 'on_grey'))
            else:
                colored_row.append(colored("_", 'white', 'on_grey'))
        print("  | " + " | ".join(colored_row) + " |")
        print("  +" + "---+" * WORD_LENGTH)

    print()
    print("Time Elapsed: {} minutes {} seconds".format(elapsed_time.seconds // 60, elapsed_time.seconds % 60))

    if reveal_word:
        print("The word was:", reveal_word)


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


# Function to play the game
def play_game():
    target_word = generate_word()
    attempts = 0
    grid = []
    start_time = datetime.now()
    end_time = start_time + timedelta(seconds=TIMER_DURATION)

    print("Welcome to Wordle!")
    print("Guess the five-letter word.")
    print("You have", MAX_ATTEMPTS, "attempts.")
    print("You have 3 minutes to complete the game.")

    while attempts < MAX_ATTEMPTS and datetime.now() <= end_time:
        elapsed_time = datetime.now() - start_time
        display_grid(grid, elapsed_time, None)
        guess = input("Enter your guess: ").lower()

        if len(guess) != WORD_LENGTH:
            print("Invalid guess. Guess should be", WORD_LENGTH, "letters long.")
            continue

        feedback = check_guess(guess, target_word)
        grid.append(feedback)

        if feedback == [{'letter': guess[i], 'color': 'green', 'visible': True} for i in range(WORD_LENGTH)]:
            elapsed_time = datetime.now() - start_time
            display_grid(grid, elapsed_time, target_word)
            print("Congratulations! You guessed the word.")
            break

        attempts += 1

    elapsed_time = datetime.now() - start_time
    if attempts == MAX_ATTEMPTS:
        display_grid(grid, elapsed_time, target_word)
        print("Sorry, you have used all your attempts.")
    elif datetime.now() > end_time:
        display_grid(grid, elapsed_time, target_word)
        print("Sorry, you ran out of time.")

    play_again = input("Do you want to play again? (yes/no): ")
    if play_again.lower() == 'yes':
        play_game()
    else:
        print("Thank you for playing Wordle!")


@app.route('/', methods=['GET', 'POST'])
def wordle():
    if request.method == 'POST':
        target_word = generate_word()
        attempts = 0
        grid = []
        start_time = datetime.now()
        end_time = start_time + timedelta(seconds=TIMER_DURATION)

        while attempts < MAX_ATTEMPTS and datetime.now() <= end_time:
            elapsed_time = datetime.now() - start_time

            guess = request.form['guess'].lower()

            if not guess:
                message = "Please enter a valid guess."
                return render_template('index.html', message=message)

            if len(guess) != WORD_LENGTH:
                message = "Invalid guess. Guess should be {} letters long.".format(WORD_LENGTH)
                return render_template('index.html', message=message)

            feedback = check_guess(guess, target_word)
            grid.append(feedback)

            if feedback == [{'letter': guess[i], 'color': 'green', 'visible': True} for i in range(WORD_LENGTH)]:
                elapsed_time = datetime.now() - start_time
                return render_template('result.html', message="Congratulations! You guessed the word.", grid=grid, elapsed_time=elapsed_time, reveal_word=target_word)

            attempts += 1

        elapsed_time = datetime.now() - start_time
        if attempts == MAX_ATTEMPTS:
            return render_template('result.html', message="Sorry, you have used all your attempts.", grid=grid, elapsed_time=elapsed_time, reveal_word=target_word)
        elif datetime.now() > end_time:
            return render_template('result.html', message="Sorry, you ran out of time.", grid=grid, elapsed_time=elapsed_time, reveal_word=target_word)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
