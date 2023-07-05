from flask import Flask, render_template, request
import random
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
    start_time = datetime.now()

    grid = []
    for _ in range(WORD_LENGTH):
        grid.append({'letter': '', 'color': 'white', 'visible': False})

    while True:
        display_grid(grid, datetime.now() - start_time, "")
        guess = input("Enter your guess: ").upper()

        if guess == "QUIT":
            break

        if guess == "REVEAL":
            display_grid(grid, datetime.now() - start_time, target_word)
            break

        if len(guess) != WORD_LENGTH:
            print("Invalid guess! Guess word should be {} letters long.".format(WORD_LENGTH))
            continue

        attempts += 1
        feedback = check_guess(guess, target_word)

        if feedback == [{'letter': guess[i], 'color': 'green', 'visible': True} for i in range(WORD_LENGTH)]:
            display_grid(grid, datetime.now() - start_time, target_word)
            print("Congratulations! You guessed the word correctly.")
            break

        if attempts >= MAX_ATTEMPTS:
            display_grid(grid, datetime.now() - start_time, target_word)
            print("You ran out of attempts. Better luck next time!")
            break

        for i in range(WORD_LENGTH):
            if not grid[i]['visible']:
                grid[i]['letter'] = guess[i]
                grid[i]['color'] = feedback[i]['color']
                grid[i]['visible'] = True

        print("Incorrect guess! Try again.")


@app.route('/')
def index():
    return render_template('index.html', word_length=WORD_LENGTH)


if __name__ == '__main__':
    app.run()
