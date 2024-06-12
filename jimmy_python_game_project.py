import tkinter as tk
import random
import json

class GameApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Guessing Game")
        self.stage = 1
        self.score = 0
        self.high_score = 0
        self.load_high_score()
        
        self.label = tk.Label(master, text="Welcome to the Guessing Game!")
        self.label.pack()
        
        self.start_button = tk.Button(master, text="Start Game", command=self.start_game)
        self.start_button.pack()
        
        self.score_label = tk.Label(master, text=f"Score: {self.score}")
        self.score_label.pack()
        
        self.high_score_label = tk.Label(master, text=f"High Score: {self.high_score}")
        self.high_score_label.pack()

    def load_high_score(self):
        try:
            with open("high_score.json", "r") as file:
                data = json.load(file)
                self.high_score = data.get("high_score", 0)
        except FileNotFoundError:
            self.high_score = 0
    
    def save_high_score(self):
        with open("high_score.json", "w") as file:
            json.dump({"high_score": self.high_score}, file)
    
    def start_game(self):
        self.label.config(text="Let's start the number guessing game!")
        self.start_button.pack_forget()
        self.start_number_guessing()

    def start_number_guessing(self):
        self.number = random.randint(1, 10)
        self.guesses_left = 3
        self.number_guess_label = tk.Label(self.master, text="Guess a number between 1 and 10:")
        self.number_guess_label.pack()
        
        self.number_entry = tk.Entry(self.master)
        self.number_entry.pack()
        
        self.number_submit_button = tk.Button(self.master, text="Submit", command=self.check_number_guess)
        self.number_submit_button.pack()
        
        self.hint_label = tk.Label(self.master, text="")
        self.hint_label.pack()
        
    def check_number_guess(self):
        guess = int(self.number_entry.get())
        self.guesses_left -= 1
        
        if guess < self.number:
            self.hint_label.config(text="Too low, try again!")
        elif guess > self.number:
            self.hint_label.config(text="Too high, try again!")
        else:
            self.score += 10
            self.update_score()
            self.number_guess_label.pack_forget()
            self.number_entry.pack_forget()
            self.number_submit_button.pack_forget()
            self.hint_label.pack_forget()
            self.label.config(text="Correct! Moving to the next stage.")
            self.master.after(2000, self.start_word_guessing)
            return
        
        if self.guesses_left == 0:
            self.number_guess_label.pack_forget()
            self.number_entry.pack_forget()
            self.number_submit_button.pack_forget()
            self.hint_label.pack_forget()
            self.label.config(text=f"Game over! The number was {self.number}.")
            self.check_high_score()
            self.master.after(2000, self.reset_game)
    
    def start_word_guessing(self):
        self.word_list = {
            "python": "A type of large snake or a programming language",
            "apple": "A fruit or a tech company",
            "guitar": "A musical instrument with strings"
        }
        self.word, self.hint = random.choice(list(self.word_list.items()))
        self.word_guess_label = tk.Label(self.master, text=f"Guess the word: {self.hint}")
        self.word_guess_label.pack()
        
        self.word_entry = tk.Entry(self.master)
        self.word_entry.pack()
        
        self.word_submit_button = tk.Button(self.master, text="Submit", command=self.check_word_guess)
        self.word_submit_button.pack()
        
        self.word_hint_label = tk.Label(self.master, text="")
        self.word_hint_label.pack()

    def check_word_guess(self):
        guess = self.word_entry.get().strip().lower()
        
        if guess == self.word:
            self.score += 20
            self.update_score()
            self.word_guess_label.pack_forget()
            self.word_entry.pack_forget()
            self.word_submit_button.pack_forget()
            self.word_hint_label.pack_forget()
            self.label.config(text="Correct! You win!")
            self.check_high_score()
            self.master.after(2000, self.reset_game)
        else:
            self.word_hint_label.config(text="Wrong, try again!")

    def update_score(self):
        self.score_label.config(text=f"Score: {self.score}")

    def check_high_score(self):
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()
            self.high_score_label.config(text=f"High Score: {self.high_score}")

    def reset_game(self):
        self.score = 0
        self.update_score()
        self.start_button.pack()
        self.label.config(text="Welcome to the Guessing Game!")
        self.word_guess_label.pack_forget()
        self.word_entry.pack_forget()
        self.word_submit_button.pack_forget()
        self.word_hint_label.pack_forget()

root = tk.Tk()
app = GameApp(root)
root.mainloop()
