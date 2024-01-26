import tkinter as tk
import random
import time

morse_codes = {
    ".-": 'a', "-...": 'b', "-.-.": 'c', "-..": 'd', ".": 'e',
    "..-.": 'f', "--.": 'g', "....": 'h', "..": 'i', ".---": 'j',
    "-.-": 'k', ".-..": 'l', "--": 'm', "-.": 'n', "---": 'o',
    ".--.": 'p', "--.-": 'q', ".-.": 'r', "...": 's', "-": 't',
    "..-": 'u', "...-": 'v', ".--": 'w', "-..-": 'x', "-.--": 'y',
    "--..": 'z'
}

class MorseGameGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("MorseZone Game")
        self.current_game_window = None
        self.score = 0

        self.label = tk.Label(master, text="Welcome to the MorseZone!", font=("Helvetica", 16))
        self.label.grid(row=0, column=0, pady=20)

        self.start_button = tk.Button(master, text="Start Game", command=self.start_game, font=("Helvetica", 14))
        self.start_button.grid(row=1, column=0, pady=10)

        self.hint_button = tk.Button(master, text="Hint", command=self.display_hint, font=("Helvetica", 14))
        self.hint_button.grid(row=2, column=0, pady=10)

        self.quit_button = tk.Button(master, text="Quit", command=self.master.destroy, font=("Helvetica", 14))
        self.quit_button.grid(row=3, column=0, pady=10)

    def start_game(self):
        if self.current_game_window:
            self.current_game_window.destroy()

        self.current_game_window = tk.Toplevel(self.master)
        self.score = 0
        self.questions_attempted = 0
        self.start_time = time.time()
        self.display_next_question()

    def display_next_question(self):
        if time.time() - self.start_time <= 30:  # Check if 30 seconds have not passed
            random_morse, correct_answer = random.choice(list(morse_codes.items()))
            self.display_question(random_morse)

            user_input = tk.Entry(self.current_game_window, font=("Helvetica", 14))
            user_input.grid(row=2, column=0, pady=10)

            submit_button = tk.Button(self.current_game_window, text="Submit", command=lambda r=random_morse, c=correct_answer: self.check_answer(user_input, r, c), font=("Helvetica", 14))
            submit_button.grid(row=3, column=0, pady=10)
        else:
            self.display_score()

    def check_answer(self, user_input, random_morse, correct_answer):
        user_answer = user_input.get().lower()
        user_input.delete(0, tk.END)

        if user_answer == correct_answer:
            self.score += 1
        self.questions_attempted += 1
        self.display_next_question()

    def display_question(self, random_morse):
        morse_label = tk.Label(self.current_game_window, text=f"Guess the letter for the following Morse code:\n{random_morse}", font=("Helvetica", 14))
        morse_label.grid(row=1, column=0, pady=20)

    def display_score(self):
        score_label = tk.Label(self.current_game_window, text=f"Your final score is: {self.score}/{self.questions_attempted}", font=("Helvetica", 16))
        score_label.grid(row=2, column=0, pady=20)

    def display_hint(self):
        hint_window = tk.Toplevel(self.master)
        hint_window.title("Morse Code Hints")

        hint_label = tk.Label(hint_window, text=self.generate_hint_text(), font=("Helvetica", 14))
        hint_label.pack(pady=20)

        back_button = tk.Button(hint_window, text="Back", command=hint_window.destroy, font=("Helvetica", 14))
        back_button.pack(pady=10)

    def generate_hint_text(self):
        hint_text = "Morse Code Hints:\n"
        for code, letter in morse_codes.items():
            hint_text += f"{letter.upper()} = {code}\n"
        return hint_text

if __name__ == "__main__":
    root = tk.Tk()
    app = MorseGameGUI(root)
    root.mainloop()
