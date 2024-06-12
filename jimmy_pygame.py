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
FONT = pygame.font.Font(None, 20)  # Reduce the font size to 28

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
    max_attempts = 3  # Reduced the number of guesses to 3
    score = 0
    input_active = True
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
                        if input_text.isdigit():
                            guess = int(input_text)
                            attempts += 1
                            input_text = ''
                            if guess < number:
                                message = "Your guess is too low!"
                            elif guess > number:
                                message = "Your guess is too high!"
                            else:
                                message = f"Congratulations {player_name}, you guessed the number in {attempts} tries!"
                                score = (max_attempts - attempts + 1) * 10
                                return score, True
                        else:
                            message = "Please enter a valid number."
                    elif event.key == K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
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
def word_guessing_game(screen, player_name, used_words):
    words = {
        'python': 'A high-level programming language.',
        'pygame': 'A set of Python modules designed for writing video games.',
        'computer': 'An electronic device for storing and processing data.',
        'internet': 'A global computer network providing a variety of information and communication facilities.',
        'keyboard': 'An input device that uses keys to input characters into a computer.',
        'monitor': 'An output device that displays information in pictorial form.'
    }

    # Filter out used words
    available_words = {word: hint for word, hint in words.items() if word not in used_words}
    
    if not available_words:
        return 0, False  # No words left to guess

    word, hint = random.choice(list(available_words.items()))
    max_attempts = 3  # Reduced the number of guesses to 3
    attempts = 0
    guessed_letters = set()
    input_active = True
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
                        guess = input_text.lower()
                        attempts += 1
                        input_text = ''
                        if guess == word:
                            message = f"Congratulations {player_name}, you guessed the word!"
                            score = (max_attempts - attempts + 1) * 20
                            used_words.add(word)
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
    lives = 3
    used_words = set()  # Keep track of used words

    while lives > 0:
        score, won = number_guessing_game(screen, player_name)
        total_score += score
        if not won:
            lives -= 1
            continue

        score, won = word_guessing_game(screen, player_name, used_words)
        total_score += score
        if not won:
            lives -= 1
            continue

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
                        lives = 3
                        used_words.clear()  # Reset used words for new game
                    if event.key == K_q:
                        pygame.quit()
                        sys.exit()

if __name__ == "__main__":
    main()
