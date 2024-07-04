import random
import os
import sys


def get_resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def get_answer():
    words = open(get_resource_path('answers-wordlist.txt')).read().splitlines()
    return random.choice(words)


def check_valid(guess):
    valid_guesses = open(get_resource_path('valid-wordlist.txt')).read().splitlines()
    return len(guess) == 5 and guess in valid_guesses

# '\033[93m' - yellow
# '\033[92m' - green
# '\033[39m' - grey / reset


def format_answer_string(validated_answer):
    colors = {
        0: '\033[39m',  # grey/reset
        1: '\033[93m',  # yellow
        2: '\033[92m'   # green
    }

    answer_string = ''
    for i in validated_answer:
        color = colors[i[1]]
        answer_string += color + ' ' + i[0] + '\033[39m'
    return answer_string


def check_guess(guess, answer):
    result = []
    letter_count = {}

    for letter in guess:
        result.append([letter, 0])

    for i in range(len(guess)):
        if guess[i] == answer[i]:
            result[i] = [guess[i], 2]
        else:
            if answer[i] in letter_count:
                letter_count[answer[i]] += 1
            else:
                letter_count[answer[i]] = 1

    for i in range(len(guess)):
        if result[i][1] == 2:
            continue
        if guess[i] in letter_count and letter_count[guess[i]] > 0:
            result[i] = [guess[i], 1]
            letter_count[guess[i]] -= 1
    return result


def guess(guess_number, answer):
    guess_input = input('Guess ' + str(guess_number + 1) + ': ')
    if not check_valid(guess_input):
        print('NO! Invalid guess loser, try again')
        guess(guess_number, answer)
    else:
        validated_input = check_guess(guess_input, answer)
        print(format_answer_string(validated_input))
        if guess_input == answer:
            return True
        else:
            return False


def start_game():
    answer = get_answer()
    failed = True
    print('Whatsup nerd, welcome to wordle')
    for i in range(6):
        done = guess(i, answer)
        if done:
            print('Nice! you got it in ' + str(i + 1) + ' guess(es)!')
            failed = False
            break

    if failed:
        print('Lmao you failed, you suck.')
        print('The answer was ' + str(answer) + ' btw ;)')

    while True:
        again = input('Would you like to play again? Y or N: ')
        if again.lower() == 'y':
            start_game()
        elif again.lower() == 'n':
            print('Thanks, cya later')
            return


if __name__ == "__main__":
    try:
        start_game()
    except Exception as e:
        print(f"An error occurred: {e}")
    input("Press Enter to close the program...")


# build command
# pyinstaller --onefile --add-data "C:\Users\nomis\PycharmProjects\wordle\wordle-game\answers-wordlist.txt;." --add-data "C:\Users\nomis\PycharmProjects\wordle\wordle-game\valid-wordlist.txt;." --distpath dist wordle-game.py
