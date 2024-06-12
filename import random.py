import pygame
import random
import sys
import json
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Font
FONT = pygame.font.Font(None, 36)

# Load high scores
def load_high_scores():
    try:
        with open('high_scores.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Save high scores
def save_high_scores(high_scores):
    with open('high_scores.json', 'w') as file:
        json.dump(high_scores, file)

# Display text on the screen
def display_text(screen, text, x, y, color=BLACK):
    text_surface = FONT.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Number guessing game
def number_guessing_game(screen, player_name):
    number = random.randint(1, 10)
    attempts = 0
    max_attempts = 5
    score = 0
    input_active = False
    input_text = ''
    message = f"Guess a number between 1 and 10. You have {max_attempts} attempts."

    while attempts < max_attempts:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if input_active:
                    if event.key == K_RETURN:
                        attempts += 1
                        guess = int(input_text)
                        input_text = ''
                        if guess < number:
                            message = "Your guess is too low!"
                        elif guess > number:
                            message = "Your guess is too high!"
                        else:
                            message = f"Congratulations {player_name}, you guessed the number in {attempts} tries!"
                            score = (max_attempts - attempts + 1) * 10
                            return score, True
                    elif event.key == K_BACKSPACE:
                        input_text = input_text[:-1]
                    elif event.unicode.isdigit():
                        input_text += event.unicode

        screen.fill(WHITE)
        display_text(screen, message, 20, 20)
        display_text(screen, f'Your guess: {input_text}', 20, 60)
        pygame.display.update()

    message = f"You couldn't guess the number. It was {number}."
    screen.fill(WHITE)
    display_text(screen, message, 20, 20)
    pygame.display.update()
    pygame.time.wait(2000)

    return score, False

# Word guessing game
def word_guessing_game(screen, player_name):
    words = {
        'python': 'A high-level programming language.',
        'pygame': 'A set of Python modules designed for writing video games.',
        'computer': 'An electronic device for storing and processing data.'
    }
    word, hint = random.choice(list(words.items()))
    max_attempts = 5
    attempts = 0
    guessed_letters = set()
    input_active = False
    input_text = ''
    score = 0
    message = f"Guess the word. Hint: {hint}. You have {max_attempts} attempts."

    while attempts < max_attempts:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if input_active:
                    if event.key == K_RETURN:
                        attempts += 1
                        guess = input_text.lower()
                        input_text = ''
                        if guess == word:
                            message = f"Congratulations {player_name}, you guessed the word!"
                            score = (max_attempts - attempts + 1) * 20
                            return score, True
                        else:
                            guessed_letters.add(guess)
                            message = "Incorrect guess!"
                    elif event.key == K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        input_text += event.unicode

        screen.fill(WHITE)
        display_text(screen, message, 20, 20)
        display_text(screen, f'Your guess: {input_text}', 20, 60)
        display_text(screen, f'Guessed letters: {", ".join(guessed_letters)}', 20, 100)
        display_text(screen, f'Word: {" ".join([letter if letter in guessed_letters else "_" for letter in word])}', 20, 140)
        pygame.display.update()

    message = f"You couldn't guess the word. It was {word}."
    screen.fill(WHITE)
    display_text(screen, message, 20, 20)
    pygame.display.update()
    pygame.time.wait(2000)

    return score, False

# Main function
def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Guessing Game')

    high_scores = load_high_scores()
    player_name = input("Enter your name: ")
    total_score = 0

    while True:
        score, won = number_guessing_game(screen, player_name)
        total_score += score
        if not won:
            break

        score, won = word_guessing_game(screen, player_name)
        total_score += score
        if not won:
            break

        if total_score > max(high_scores, default=0):
            high_scores.append(total_score)
            high_scores.sort(reverse=True)
            save_high_scores(high_scores)

        screen.fill(WHITE)
        display_text(screen, f'Game over, {player_name}! Your final score is: {total_score}', 20, 20)
        display_text(screen, 'High Scores:', 20, 60)
        for i, high_score in enumerate(high_scores[:5], start=1):
            display_text(screen, f'{i}. {high_score}', 20, 60 + i * 30)
        display_text(screen, 'Press R to play again or Q to quit.', 20, 220)
        pygame.display.update()

        replay = False
        while not replay:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_r:
                        replay = True
                        total_score = 0
                    if event.key == K_q:
                        pygame.quit()
                        sys.exit()

if __name__ == "__main__":
    main()
