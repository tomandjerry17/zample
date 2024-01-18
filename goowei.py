import tkinter as tk
from tkinter import messagebox
import random
import time
import sqlite3

class MorseGameGUI:
    # Define Morse code patterns and their corresponding letters
    morse_codes = {".-": 'a', "-...": 'b', "-.-.": 'c', "-..": 'd', ".": 'e',
                   "..-.": 'f', "--.": 'g', "....": 'h',
                   "..": 'i', ".---": 'j', "-.-": 'k', ".-..": 'l', "--": 'm',
                   "-.": 'n', "---": 'o', ".--.": 'p',
                   "--.-": 'q', ".-.": 'r', "...": 's', "-": 't', "..-": 'u',
                   "...-": 'v', ".--": 'w', "-..-": 'x',
                   "-.--": 'y', "--..": 'z'}

    def __init__(self, root):
        self.root = root
        self.root.title("MorseZone Game")

        self.label = tk.Label(root, text="Welcome to the MorseZone!")
        self.label.pack()

        self.button_frame = tk.Frame(root)
        self.button_frame.pack()

        self.normal_button = tk.Button(self.button_frame, text="Normal Mode", command=self.start_normal_game)
        self.normal_button.grid(row=0, column=0, padx=10, pady=10)

        self.timed_button = tk.Button(self.button_frame, text="Timed Mode", command=self.start_timed_game)
        self.timed_button.grid(row=0, column=1, padx=10, pady=10)

        self.high_scores_button = tk.Button(self.button_frame, text="High Scores", command=self.display_high_scores)
        self.high_scores_button.grid(row=1, column=0, columnspan=2, pady=10)

        self.quit_button = tk.Button(self.button_frame, text="Quit", command=self.root.destroy)
        self.quit_button.grid(row=2, column=0, columnspan=2, pady=10)

    def start_normal_game(self):
        self.start_game('Normal')

    def start_timed_game(self):
        self.start_game('Timed')

    def start_game(self, game_mode):
        self.root.withdraw()  # Hide the main window

        game_window = tk.Toplevel(self.root)
        game_window.title(f"{game_mode} Mode")

        if game_mode == 'Normal':
            self.normal_game(game_window)
        elif game_mode == 'Timed':
            self.timed_game(game_window)

    def normal_game(self, game_window):
        # Initialize the score
        score = 0

        for _ in range(10):
            # Randomly select a Morse code pattern
            random_morse = random.choice(list(self.morse_codes.keys()))

            # Display Morse code to the user
            morse_label = tk.Label(game_window, text=f"Guess the letter for the following Morse code:\n{random_morse}")
            morse_label.pack()

            # Get user input
            user_input = tk.Entry(game_window)
            user_input.pack()

            # Submit button
            submit_button = tk.Button(game_window, text="Submit", command=lambda: self.check_answer(game_window, user_input, random_morse, score))
            submit_button.pack()

            game_window.wait_window()

        # Display final score
        messagebox.showinfo("Game Over", f"Your final score is: {score}")
        store_score("Player", score, 'Normal')

        self.root.deiconify()  # Show the main window

    def timed_game(self, game_window):
        # Initialize Score
        score = 0

        # Setting the time limit
        game_duration = 30

        # Formula
        end_time = time.time() + game_duration

        while time.time() < end_time:
            # Randomly select a Morse code pattern
            random_morse = random.choice(list(self.morse_codes.keys()))

            # Display remaining time and Morse code
            remaining_time_label = tk.Label(game_window, text=f"Remaining time: {int(end_time - time.time())} seconds")
            remaining_time_label.pack()

            morse_label = tk.Label(game_window, text=f"Guess the letter for the following Morse code:\n{random_morse}")
            morse_label.pack()

            # Get user input
            user_input = tk.Entry(game_window)
            user_input.pack()

            # Submit button
            submit_button = tk.Button(game_window, text="Submit", command=lambda: self.check_answer(game_window, user_input, random_morse, score))
            submit_button.pack()

            game_window.wait_window()

        # Display final score
        messagebox.showinfo("Game Over", f"Time's up! Your total score is {score}")
        store_score("Player", score, 'Timed')

        self.root.deiconify()  # Show the main window

    def check_answer(self, game_window, user_input, random_morse, score):
        user_answer = user_input.get().lower()
        correct_answer = self.morse_codes[random_morse]

        if user_answer == correct_answer:
            messagebox.showinfo("Correct", "Nice! You guessed it correctly!")
            score += 1
        else:
            messagebox.showinfo("Wrong", f"Wrong. The correct answer is '{correct_answer}'.")

        game_window.destroy()  # Close the game window

    def display_high_scores(self):
        conn = sqlite3.connect('morse_game.db')
        cursor = conn.cursor()

        # Fetch and display high scores
        cursor.execute('''
            SELECT player_name, score, game_mode, timestamp
            FROM scores
            ORDER BY score DESC
            LIMIT 10
        ''')

        high_scores = cursor.fetchall()

        high_scores_str = "\n".join([f"{name}: {score} points ({mode} mode) - {timestamp}" for name, score, mode, timestamp in high_scores])

        messagebox.showinfo("High Scores", high_scores_str)

        conn.close()


if __name__ == "__main__":
    root = tk.Tk()
    app = MorseGameGUI(root)
    root.mainloop()
