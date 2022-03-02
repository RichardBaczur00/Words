import random
import pandas as pd
from termcolor import colored


def read_dataset():
    data = pd.read_csv('./words.csv')
    data['word'] = data.values.sum(axis=1)
    return pd.DataFrame(data['word'])


def choose_word(words):
    chosen_index = random.randint(0, len(words))
    return words.loc[chosen_index].values


def validate_input(player, words):
    if len(player) != 5:
        print('Your word is longer than 5 letters! The word must be composed of 5 letters.')
        return False

    if not words.word.str.contains(player).any():
        print('Your word is not a valid word. Words must be in english (might be the dataset, try something else instead)')
        return False

    return True


def check_word(player_word, expected):
    if player_word == expected:
        return True

    for i in range(5):
        if player_word[i] == expected[i]:
            print(colored(player_word[i], 'green'), end='')
        elif player_word[i] in expected:
            print(colored(player_word[i], 'blue'), end='')
        else:
            print(player_word[i], end='')
    print()

    return False



def main():
    lives = 6
    words = read_dataset()
    chosen_word = choose_word(words)[0]
    print(words.head())
    print('Welcome to infinite wordle!')
    print('You must chose a 5 letter word. The game will tell you if you have correct letters in corrent positions or correct letters in incorrect positions.')
    print('Using this information, you must guess the word in 6 (or less) tries. Good luck!')

    while True:
        player_word = input()

        if not validate_input(player_word, words):
            continue

        if check_word(player_word, chosen_word):
            print(f'Correct: {colored(player_word, "green")}')
            break
        else:
            lives -= 1
            if lives == 0:
                print('Out of tries!')
                print(f'Word was {chosen_word}')
                break
            print(f'You have {lives} tries left.')


if __name__ == '__main__':
    main()
