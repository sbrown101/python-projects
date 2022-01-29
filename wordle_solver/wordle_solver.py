import copy
import random


def generate_word_list():
    with open('words.txt') as f:
        word_list = [word.rstrip() for word in f]
    return word_list


def sanitise_input(input):
    return input.lower().translate({ord(i): None for i in ', '})


def validate_letters(word, letters):
    if letters == '':
        return True
    for letter in letters:
        if letter not in word:

            return False
        else:
            return True


def new_game():
    still_playing = True
    word_list = WordList()
    print("Let's play some Wordle!")
    while still_playing:
        try:
            new_turn(word_list)
        except IndexError:
            print("Sorry, I don't know the word.")
            still_playing = False


def new_turn(word_list):
    current_word = word_list.guess_word()

    print(f"Try {current_word}")
    has_entered_valid_string = False
    while not has_entered_valid_string:
        correct_letters = sanitise_input(input("Were any letters correct? Type them or press enter for no "))
        has_entered_valid_string = validate_letters(current_word, correct_letters)
        if not has_entered_valid_string:
            print(f"Please only enter letters from the suggested word ({current_word}).")

    for letter in current_word:
        if letter in correct_letters:
            word_list.remove_words_without_letter(letter)
        else:
            word_list.remove_words_with_letter(letter)

    has_entered_valid_string = False
    while len(correct_letters) > 0 and not has_entered_valid_string:
        correct_positions = sanitise_input(
            input("Were any letters in the correct positions? Type them or press enter for no "))
        has_entered_valid_string = validate_letters(correct_letters, correct_positions)
        if not has_entered_valid_string:
            print(f"Please only enter letters we know are right ({correct_letters}).")


        for letter in current_word:
            if letter in correct_positions:
                word_list.remove_words_without_letter_at_index(letter, current_word.index(letter))
            else:
                word_list.remove_words_with_letter_at_index(letter, current_word.index(letter))

    word_list.print_list()


class WordList:
    def __init__(self):
        self.words = generate_word_list()

    def print_list(self):
        for line in self.words:
            print(line)

    def guess_word(self):
        return random.choice(self.words)

    def remove_words_with_letter(self, letter):
        new_word_list = copy.deepcopy(self.words)
        for word in self.words:
            if letter in word:
                new_word_list.remove(word)
        self.words = new_word_list

    def remove_words_with_letter_at_index(self, letter, index):
        new_word_list = copy.deepcopy(self.words)
        for word in self.words:
            if word[index] == letter:
                new_word_list.remove(word)
        self.words = new_word_list

    def remove_words_without_letter(self, letter):
        new_word_list = copy.deepcopy(self.words)
        for word in self.words:
            if letter not in word:
                new_word_list.remove(word)
        self.words = new_word_list

    def remove_words_without_letter_at_index(self, letter, index):
        new_word_list = copy.deepcopy(self.words)
        for word in self.words:
            if word[index] != letter:
                new_word_list.remove(word)
        self.words = new_word_list


if __name__ == '__main__':
    new_game()
