import pygame
import sys
import random
from button import Button
pygame.init()

WINDOW_SIZE = (450, 600)
window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Wordle!")

# colors
GREY = "#a0b1ac"
LIGHT_GREY = "#d8dfdc"
RED = "#ff333e"
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = "#6aaa64"
YELLOW = "#ffdb1c"

# images
wordle_logo = pygame.transform.scale(pygame.image.load("wordle_logo.png"), (322, 70))

# fonts
score_font = pygame.font.Font("Dosis-SemiBold.ttf", 50)
letter_font = pygame.font.SysFont("segoeuiemoji", 30)
notbutton_font = pygame.font.SysFont("Arial", 20, "bold")
title_font = pygame.font.SysFont("Berlin Sans FB Demi", 80, "bold")
subtitle_font = pygame.font.Font("Dosis-SemiBold.ttf", 30)

letters = [chr(i) for i in range(65, 91)]
letters.append("🔙")
keys = []

streak = 0
score = 0


class Letter:
    def __init__(self, surface, letter, x, y, square_width, square_height, square_color,
                 border_color, letter_color, letter_font, font_size, text_x, text_y):
        self.surface = surface
        self.letter = letter
        self.x = x
        self.y = y
        self.square_width = square_width
        self.square_height = square_height
        self.square_color = square_color
        self.border_color = border_color
        self.letter_color = letter_color
        self.letter_font = letter_font
        self.font_size = font_size
        self.text_x = text_x
        self.text_y = text_y

        self.font = pygame.font.SysFont(self.letter_font, self.font_size, "bold")

    def draw(self):
        pygame.draw.rect(self.surface, self.square_color, (self.x, self.y, self.square_width,
                                                           self.square_height), 0, 10)
        pygame.draw.rect(self.surface, self.border_color, (self.x, self.y, self.square_width,
                                                           self.square_height), 3, 10)
        self.surface.blit(self.font.render(self.letter, True, self.letter_color),
                          (self.text_x, self.text_y))


class Key:
    def __init__(self, surface, color, font, text_color, letter, x, y, text_x, text_y, width, height):
        self.surface = surface
        self.color = color
        self.font = font
        self.text_color = text_color
        self.letter = letter
        self.x = x
        self.y = y
        self.text_x = text_x
        self.text_y = text_y
        self.width = width
        self.height = height

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self):
        pygame.draw.rect(self.surface, self.color, self.rect)
        self.surface.blit(self.font.render(self.letter, True, self.text_color),
                          (self.text_x, self.text_y))


class GuessesBoard:
    def __init__(self, surface, start_x, start_y, guesses_num, word_len,
                 letters_padx, letters_pady):
        self.surface = surface
        self.start_x = start_x
        self.start_y = start_y
        self.guesses_num = guesses_num
        self.word_len = word_len

        self.letters_padx = letters_padx
        self.letters_pady = letters_pady

        self.words_squares = []
        self.letter_index = 0

    def create(self):
        x = self.start_x
        y = self.start_y
        for i in range(self.guesses_num):
            word_lst = []
            for j in range(self.word_len):
                letter = Letter(self.surface, "", x, y, 50, 50, LIGHT_GREY, WHITE, WHITE, "Arial",
                                25, x+15, y+10)
                word_lst.append(letter)
                x += self.letters_padx
            self.words_squares.append(word_lst)
            x = self.start_x
            y += self.letters_pady

    def draw(self):
        for word_square in self.words_squares:
            for letter in word_square:
                letter.draw()


def get_words():
    with open("words.txt", "r") as f:
        lst = f.readlines()
        lst = list(map(lambda s: s.strip(), lst))
        return lst


def choose_word():
    words = get_words()
    return random.choice(words)


def create_keyboard():
    line_len = 10
    x = 25
    y = 430
    count = 0
    for i in range(3):
        for j in range(line_len):
            count += 1
            if count == len(letters):
                width = 50
                text_x = x + 5
            else:
                width = 35
                text_x = x + 10

            key = Key(window, WHITE, letter_font, GREY, letters[count - 1], x, y,
                      text_x, y + 10, width, 50)
            keys.append(key)
            x += 40
        line_len -= 1

        if i == 0:
            x = 47
        elif i == 1:
            x = 67

        y += 55


def draw_keyboard():
    for key in keys:
        key.draw()


def backspace(index, guesses_board, guess_count):
    guesses_board.words_squares[guess_count][index - 1].letter = ""
    guesses_board.letter_index -= 1


def paint_key(letter, color):
    for key in keys:
        if key.letter == letter.upper():
            key.color = color
            key.text_color = WHITE


def end_round(game_status, word, guess_count):
    global streak, score

    streak += 1
    score += (6 - guess_count)

    play_button = Button(window, GREEN, BLACK, "PLAY", 123, 400, 200, 100, "Arial",
                         160, 420, 50, BLACK)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.rect.collidepoint(event.pos):
                    if game_status.lower() != "victory":
                        streak = 0
                        score = 0
                        menu()
                        return
                    main()

        window.fill(LIGHT_GREY)

        if game_status.lower() == "victory":
            window.blit(title_font.render(f"{game_status.upper()}!", True, WHITE), (50, 10))
        else:
            window.blit(title_font.render(f"{game_status.upper()}!", True, WHITE), (0, 10))

        window.blit(subtitle_font.render("The word was", True, WHITE), (135, 120))
        window.blit(score_font.render(word.upper(), True, YELLOW), (150, 150))
        window.blit(subtitle_font.render("Current Streak", True, WHITE), (20, 230))
        window.blit(subtitle_font.render(str(streak), True, YELLOW), (90, 270))
        window.blit(subtitle_font.render("Current Score", True, WHITE), (260, 230))
        window.blit(subtitle_font.render(str(score), True, YELLOW), (330, 270))

        play_button.draw()
        pygame.display.update()

    pygame.quit()
    sys.exit(0)


def check_word(guesses_board, guess_count, guess_word, word):
    guess_word = guess_word.lower()

    for i, (l1, l2) in enumerate(zip(guess_word, word)):
        if l1 == l2:
            guesses_board.words_squares[guess_count][i].square_color = GREEN
            paint_key(l1, GREEN)
        elif l1 in word:
            guesses_board.words_squares[guess_count][i].square_color = YELLOW
            paint_key(l1, YELLOW)
        else:
            guesses_board.words_squares[guess_count][i].square_color = GREY
            paint_key(l1, GREY)

    if word == guess_word:
        end_round("victory", word, guess_count)
    elif guess_count == 5:
        end_round("game over", word, guess_count)


def get_guess_word(guesses_board, guess_count):
    guess_word = ""
    for i in range(5):
        letter = guesses_board.words_squares[guess_count][i].letter
        guess_word += letter

    return guess_word


def main():
    guesses_board = GuessesBoard(window, 80, 60, 6, 5, 60, 60)
    guesses_board.create()
    create_keyboard()

    submit_button = Button(window, GREY, WHITE, "SUBMIT", 2, 5, 100, 50, "Arial",
                           7, 15, 25, BLACK)

    word = choose_word()
    print(word)

    not_word = False

    guess_count = 0

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                index = guesses_board.letter_index
                key_clicked = pygame.key.name(event.key)
                if index < 5 and key_clicked.isalpha() and len(key_clicked) == 1:
                    guesses_board.words_squares[guess_count][index].letter = key_clicked.upper()
                    guesses_board.letter_index += 1
                elif key_clicked == "backspace" and guesses_board.letter_index > 0:
                    backspace(index, guesses_board, guess_count)
                    not_word = False
                    submit_button.bg = GREY
                elif key_clicked == "return" and guesses_board.letter_index >= 4 and \
                        submit_button.bg == GREEN:
                    check_word(guesses_board, guess_count,
                               get_guess_word(guesses_board, guess_count), word)
                    guess_count += 1
                    guesses_board.letter_index = 0
                    not_word = False
                    submit_button.bg = GREY

            if event.type == pygame.MOUSEBUTTONDOWN:
                for key in keys:
                    index = guesses_board.letter_index
                    if key.rect.collidepoint(event.pos) and key.letter.isalpha():
                        if index < 5:
                            guesses_board.words_squares[guess_count][index].letter = key.letter
                            guesses_board.letter_index += 1
                    elif key.rect.collidepoint(event.pos) and not key.letter.isalpha() and \
                            guesses_board.letter_index > 0:
                        backspace(index, guesses_board, guess_count)
                        not_word = False
                        submit_button.bg = GREY

                if submit_button.bg == GREEN and submit_button.rect.collidepoint(event.pos):
                    check_word(guesses_board, guess_count,
                               get_guess_word(guesses_board, guess_count), word)
                    guess_count += 1
                    guesses_board.letter_index = 0
                    not_word = False
                    submit_button.bg = GREY

        window.fill(LIGHT_GREY)
        guesses_board.draw()
        draw_keyboard()
        submit_button.draw()

        if guesses_board.letter_index > 4:
            guess_word = get_guess_word(guesses_board, guess_count)
            if guess_word.lower() in get_words():
                not_word = False
                submit_button.bg = GREEN
            else:
                not_word = True

        if not_word:
            submit_button.bg = RED
            submit_button.text = "NOT A" # first line of text on the button
            submit_button.font_size = 20
            submit_button.text_y = 10
            submit_button.text_x = 18
            # second line of text on the button
            window.blit(notbutton_font.render("WORD", True, WHITE), (20, 30))
        else:
            submit_button.text = "SUBMIT"
            submit_button.font_size = 25
            submit_button.text_y = 12
            submit_button.text_x = 7

        window.blit(score_font.render(f"Score: {score}", True, GREY), (135, -5))

        pygame.display.update()

    pygame.quit()
    sys.exit(0)


def menu():
    play_button = Button(window, GREEN, BLACK, "PLAY", 123, 150, 200, 100, "Arial",
                         160, 170, 50, BLACK)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.rect.collidepoint(event.pos):
                    main()

        window.fill(WHITE)
        window.blit(wordle_logo, (65, 20))
        play_button.draw()

        pygame.display.update()

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    menu()
