import copy
import random


def generate_word_list():
    with open('words.txt') as f:
        word_list = [word.rstrip() for word in f]
    return word_list


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
