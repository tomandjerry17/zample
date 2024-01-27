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


class CountdownWindow:
    def __init__(self, master, callback):
        self.master = master
        self.callback = callback
        self.remaining_time = 30
        self.countdown_label = tk.Label(master, text=f"Time Left: {self.remaining_time} seconds", font=("Helvetica", 12))
        self.countdown_label.pack(pady=10)
        self.update_countdown()

    def update_countdown(self):
        if self.remaining_time > 0:
            self.remaining_time -= 1
            self.countdown_label.config(text=f"Time Left: {self.remaining_time} seconds")
            self.master.after(1000, self.update_countdown)
        else:
            self.callback()


class MorseGameGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("MorseZone Game")
        self.current_game_window = None
        self.timed_countdown_window = None
        self.hint_window = None
        self.score = 0

        self.label = tk.Label(master, text="Welcome to the MorseZone!", font=("Helvetica", 16))
        self.label.grid(row=0, column=0, pady=20)

        self.normal_button = tk.Button(master, text="Normal Mode", command=self.start_normal_game,
                                       font=("Helvetica", 14))
        self.normal_button.grid(row=1, column=0, pady=10)

        self.timed_button = tk.Button(master, text="Timed Mode", command=self.start_timed_game, font=("Helvetica", 14))
        self.timed_button.grid(row=2, column=0, pady=10)

        self.hint_button = tk.Button(master, text="Hint", command=self.display_hint, font=("Helvetica", 14))
        self.hint_button.grid(row=3, column=0, pady=10)

        self.quit_button = tk.Button(master, text="Quit", command=self.master.destroy, font=("Helvetica", 14))
        self.quit_button.grid(row=4, column=0, pady=10)

    def start_normal_game(self):
        if self.current_game_window:
            self.current_game_window.destroy()

        self.current_game_window = tk.Toplevel(self.master)
        self.score = 0
        self.morse_codes_copy = list(morse_codes.items())
        random.shuffle(self.morse_codes_copy)
        self.current_question_index = 0

        self.normal_display_next_question()

    def normal_display_next_question(self):
        if self.current_question_index < 10:
            random_morse, correct_answer = self.morse_codes_copy[self.current_question_index]
            self.normal_display_question(random_morse)

            user_input = tk.Entry(self.current_game_window, font=("Helvetica", 14))
            user_input.grid(row=2, column=0, pady=10)

            submit_button = tk.Button(self.current_game_window, text="Submit",
                                      command=lambda r=random_morse, c=correct_answer: self.normal_check_answer(user_input, r,
                                                                                                         c),
                                      font=("Helvetica", 14))
            submit_button.grid(row=3, column=0, pady=10)

        else:
            empty_label = tk.Label(self.current_game_window,
                                   text="                                                                                \n  ",
                                   font=("Helvetica", 14))
            empty_label.grid(row=1, column=0, pady=20)
            self.normal_display_score()
            main_menu_button = tk.Button(self.current_game_window, text="Back to Main Menu",
                                         command=self.current_game_window.destroy, font=("Helvetica", 14))
            main_menu_button.grid(row=3, column=0, pady=10)
            empty_label = tk.Label(self.current_game_window,
                                   text="                                                         \n  ",
                                   font=("Helvetica", 14))
            empty_label.grid(row=4, column=0, pady=20)

    def normal_display_question(self, random_morse):
        morse_label = tk.Label(self.current_game_window,
                               text=f"Guess the letter for the following Morse code:\n{random_morse}",
                               font=("Helvetica", 14))
        morse_label.grid(row=1, column=0, pady=20)

    def normal_check_answer(self, user_input, random_morse, correct_answer):
        user_answer = user_input.get().lower()

        if user_answer == correct_answer:
            self.display_feedback("               Correct! Nice guess!               ", True)
            self.score += 1
        else:
            self.display_feedback(f"Wrong. The correct answer is '{correct_answer}'.", False)

        user_input.delete(0, tk.END)
        self.current_question_index += 1
        self.normal_display_next_question()

    def display_feedback(self, feedback, is_correct):
        feedback_label = tk.Label(self.current_game_window, text=feedback, font=("Helvetica", 14),
                                  fg="green" if is_correct else "red")
        feedback_label.grid(row=4, column=0, pady=20)

    def normal_display_score(self):
        score_label = tk.Label(self.current_game_window, text=f"Your final score is: {self.score}/10",
                               font=("Helvetica", 16))
        score_label.grid(row=2, column=0, pady=20)

    def start_timed_game(self):
        if self.current_game_window:
            self.current_game_window.destroy()

        self.current_game_window = tk.Toplevel(self.master)
        self.score = 0
        self.questions_attempted = 0
        self.start_time = time.time()
        self.countdown_window = tk.Toplevel(self.master)
        self.countdown_window.title("Countdown")
        self.countdown_window.geometry("200x100")
        self.countdown = CountdownWindow(self.countdown_window, self.end_game)
        self.display_next_question()

    def display_next_question(self):
        if time.time() - self.start_time <= 30:  # Check if 30 seconds have not passed
            random_morse, correct_answer = random.choice(list(morse_codes.items()))
            self.display_question(random_morse)

            user_input = tk.Entry(self.current_game_window, font=("Helvetica", 14))
            user_input.grid(row=2, column=0, pady=10)

            submit_button = tk.Button(self.current_game_window, text="Submit",
                                      command=lambda r=random_morse, c=correct_answer: self.check_answer(user_input, r,
                                                                                                         c),
                                      font=("Helvetica", 14))
            submit_button.grid(row=3, column=0, pady=10)

        else:
            self.end_game()

    def check_answer(self, user_input, random_morse, correct_answer):
        user_answer = user_input.get().lower()
        user_input.delete(0, tk.END)

        feedback = tk.Label(self.current_game_window, font=("Helvetica", 14))

        if user_answer == correct_answer:
            self.score += 1
            feedback.config(text="               Correct! Nice guess!               ", fg="green")
        else:
            feedback.config(text=f"Wrong. The correct answer is '{correct_answer}'.", fg="red")

        feedback.grid(row=5, column=0, pady=10)

        self.questions_attempted += 1
        self.display_next_question()

    def display_question(self, random_morse):
        morse_label = tk.Label(self.current_game_window,
                               text=f"Guess the letter for the following Morse code:\n{random_morse}",
                               font=("Helvetica", 14))
        morse_label.grid(row=1, column=0, pady=20)

    def end_game(self):
        if self.countdown_window:
            self.countdown_window.destroy()

        empty_label = tk.Label(self.current_game_window,
                               text="                                                                                \n  ",
                               font=("Helvetica", 14))
        empty_label.grid(row=1, column=0, pady=20)
        self.display_score()
        empty_label = tk.Label(self.current_game_window,
                               text="                                                         \n  ",
                               font=("Helvetica", 14))
        empty_label.grid(row=5, column=0, pady=20)
        self.remove_submit_button()

    def remove_submit_button(self):
        for widget in self.current_game_window.winfo_children():
            if widget.winfo_class() == "Button" and widget["text"] == "Submit":
                widget.destroy()

        back_to_menu_button = tk.Button(self.current_game_window, text="Back to Menu", command=self.current_game_window.destroy,
                                        font=("Helvetica", 14))
        back_to_menu_button.grid(row=4, column=0, pady=10)

    def display_score(self):
        score_label = tk.Label(self.current_game_window,
                               text=f"    Your final score is: {self.score}/{self.questions_attempted}    ",
                               font=("Helvetica", 16))
        score_label.grid(row=2, column=0, pady=20)

    def display_hint(self):
        if self.hint_window:
            self.hint_window.destroy()

        self.hint_window = tk.Toplevel(self.master)
        hint_label = tk.Label(self.hint_window, text=self.generate_hint_text(), font=("Helvetica", 12))
        hint_label.grid(row=0, column=0, pady=20)

        back_button = tk.Button(self.hint_window, text="Back to Main Menu", command=self.hint_window.destroy,
                                font=("Helvetica", 14))
        back_button.grid(row=1, column=0, pady=10)

    def generate_hint_text(self):
        hint_text = "Morse Code Hints:\n"
        for code, letter in morse_codes.items():
            hint_text += f"{letter.upper()} = {code}\n"
        return hint_text


if __name__ == "__main__":
    root = tk.Tk()
    app = MorseGameGUI(root)
    root.mainloop()
