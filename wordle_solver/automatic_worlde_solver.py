import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, \
    ElementNotVisibleException, TimeoutException
from selenium.webdriver.support.wait import WebDriverWait

from pyshadow.main import Shadow

from word_list import WordList


class AutomaticGame:
    def __init__(self):
        profile_path = r'C:/Users/Gazebo/AppData/Roaming/Mozilla/Firefox/Profiles/yx0i74ol.default'
        options = Options()
        options.set_preference('profile', profile_path)
        service = Service(r'C:/Program Files (x86)/GeckoDriver/geckodriver.exe')

        self.driver = webdriver.Firefox(service=service, options=options)
        self.shadow = Shadow(self.driver)
        self.driver.get('https://www.nytimes.com/games/wordle/index.html')
        self.driver.maximize_window()

        self.word_list = WordList()
        self.current_word = None
        self.keyboard = None
        self.board = None

    def start_new_auto_game(self):
        running = True
        self.close_popups()
        self.keyboard = self.shadow.find_element('div#keyboard')
        self.board = self.shadow.find_element('game-theme-manager div#game div#board-container div#board')

        while running:
            self.current_word = self.word_list.guess_word()
            self.type_current_word_guess()
            self.analyse_board()
            pass

    def close_popups(self):
        self.reject_cookies()
        self.close_tutorial()

    def reject_cookies(self):
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR,
                     "html body div#pz-gdpr div#pz-gdpr-banner div#pz-gdpr-btns button#pz-gdpr-btn-reject"))).click()
        except TimeoutException:
            print("Could not reject cookies")

    def close_tutorial(self):
        try:
            close_icon = self.shadow.find_element("div.overlay div.content div.close-icon")
            close_icon.click()
        except NoSuchElementException:
            print("Could not close tutorial")

    def type_current_word_guess(self):
        for letter in self.current_word:
            for row in self.keyboard.find_elements(By.CLASS_NAME, 'row'):
                for button in row.find_elements(By.TAG_NAME, 'button'):
                    if letter == button.get_attribute('data-key'):
                        button.click()
        self.keyboard.find_element(By.CSS_SELECTOR, 'button.one-and-a-half:nth-child(1)').click()
        time.sleep(2)

    def analyse_board(self):
        solved = True
        ignored_letters = ''  # This is required to prevent double letters from being removed completely if only one instance of the letter is correct
        row = self.find_row_with_most_recent_guess(self.board)
        for tile in enumerate(row.find_elements(By.TAG_NAME, 'game-tile')):
            letter = tile[1].get_attribute('letter')
            if letter not in ignored_letters and tile[1].get_attribute('evaluation') == 'absent':
                solved = False
                self.word_list.remove_words_with_letter(letter)
            if tile[1].get_attribute('evaluation') == 'present':
                solved = False
                ignored_letters += letter
                self.word_list.remove_words_without_letter(letter)
                self.word_list.remove_words_with_letter_at_index(letter, tile[0])
            elif tile[1].get_attribute('evaluation') == 'correct':
                ignored_letters += letter
                self.word_list.remove_words_without_letter_at_index(letter, tile[0])

        if solved:
            print("Congratulations, You win!")
            exit(0)

    def find_row_with_most_recent_guess(self, board):
        for row in reversed(board.find_elements(By.TAG_NAME, 'game-row')):
            if len(row.get_attribute('letters')) > 0:
                return self.shadow.find_element(row, 'div.row')


if __name__ == '__main__':
    game = AutomaticGame()
    game.start_new_auto_game()
