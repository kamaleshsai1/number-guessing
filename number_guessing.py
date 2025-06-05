import random
import tkinter as tk
from tkinter import font

class NumberGuessingGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Number Guessing Game")
        
        # Set the window to full screen
        self.master.attributes('-fullscreen', True)
        self.master.configure(bg="#e0f7fa")

        self.target_number = random.randint(1, 100)
        self.attempts = 0
        self.max_attempts = 10

        # Fonts used in app and in dialogs
        self.custom_font = font.Font(family="Helvetica", size=20)
        self.large_font = font.Font(family="Helvetica", size=24)
        self.dialog_font = font.Font(family="Helvetica", size=22, weight="bold")
        self.dialog_msg_font = font.Font(family="Helvetica", size=18)

        self.create_widgets()

    def create_widgets(self):
        self.instruction_label = tk.Label(self.master, text="Guess a number between 1 and 100", font=self.large_font, bg="#e0f7fa")
        self.instruction_label.pack(pady=30)

        self.guess_entry = tk.Entry(self.master, font=self.custom_font, width=10, justify='center')
        self.guess_entry.pack(pady=20)

        self.submit_button = tk.Button(self.master, text="Submit Guess", command=self.check_guess, font=self.custom_font, bg="#4CAF50", fg="white", activebackground="#45a049", activeforeground="white", padx=10, pady=5)
        self.submit_button.pack(pady=30)

        self.attempts_label = tk.Label(self.master, text=f"Attempts left: {self.max_attempts}", font=self.custom_font, bg="#e0f7fa")
        self.attempts_label.pack(pady=20)

        self.reset_button = tk.Button(self.master, text="Reset Game", command=self.reset_game, font=self.custom_font, bg="#f44336", fg="white", activebackground="#d32f2f", activeforeground="white", padx=10, pady=5)
        self.reset_button.pack(pady=20)

        self.exit_instruction_label = tk.Label(self.master, text="Press ESC to exit full screen", font=self.large_font, bg="#e0f7fa")
        self.exit_instruction_label.pack(pady=30)

        self.master.bind("<Escape>", self.exit_fullscreen)

    def show_custom_message(self, title, message, msg_type="info"):
        dialog = tk.Toplevel(self.master)
        dialog.transient(self.master)
        dialog.grab_set()
        dialog.configure(bg="#ffffff")
        dialog.title(title)

        # Remove the raised border and dark lines by setting relief flat and borderwidth 0
        frame = tk.Frame(dialog, bg="#ffffff", padx=25, pady=25, relief='flat', borderwidth=0)
        frame.pack()

        # Only create and pack icon label for warning and error messages
        if msg_type == "warning":
            icon_label = tk.Label(frame, bg="#ffffff", text="\u26A0", font=("Helvetica", 48), fg="#FF9800")
            icon_label.pack(pady=(0,10))
        elif msg_type == "error":
            icon_label = tk.Label(frame, bg="#ffffff", text="\u2716", font=("Helvetica", 48), fg="#f44336")
            icon_label.pack(pady=(0,10))
        # For "info", no icon label is created or packed.

        title_color = {"info":"#0B8043", "warning":"#FF9800", "error":"#f44336"}.get(msg_type, "#000000")
        title_label = tk.Label(frame, text=title, font=self.dialog_font, bg="#ffffff", fg=title_color)
        title_label.pack(pady=(0,15))

        message_label = tk.Label(frame, text=message, font=self.dialog_msg_font, bg="#ffffff", wraplength=380, justify="center")
        message_label.pack(pady=(0,20))

        def on_ok():
            dialog.grab_release()
            dialog.destroy()
        ok_button = tk.Button(frame, text="OK", command=on_ok, font=self.custom_font, bg=title_color, fg="white",
                              activebackground=title_color, activeforeground="white", width=12, padx=5, pady=5)
        ok_button.pack()

        dialog.update_idletasks()
        w = dialog.winfo_width()
        h = dialog.winfo_height()
        x = self.master.winfo_rootx() + (self.master.winfo_width() - w) // 2
        y = self.master.winfo_rooty() + (self.master.winfo_height() - h) // 2
        dialog.geometry(f"{w}x{h}+{x}+{y}")

        dialog.wait_window()

    def check_guess(self):
        try:
            guess = int(self.guess_entry.get())
            self.attempts += 1

            if guess < 1 or guess > 100:
                self.show_custom_message("Invalid Input", "Please enter a number between 1 and 100.", "warning")
                return

            if guess < self.target_number:
                self.show_custom_message("Result", "Too low! Try again.", "info")
            elif guess > self.target_number:
                self.show_custom_message("Result", "Too high! Try again.", "info")
            else:
                self.show_custom_message("Result", "Congratulations! You guessed the number!", "info")
                self.reset_game()
                return

            if self.attempts >= self.max_attempts:
                self.show_custom_message("Game Over", f"You've used all your attempts! The number was {self.target_number}.", "info")
                self.reset_game()
            else:
                self.attempts_label.config(text=f"Attempts left: {self.max_attempts - self.attempts}")

        except ValueError:
            self.show_custom_message("Error", "Please enter a valid integer.", "error")

        self.guess_entry.delete(0, tk.END)

    def reset_game(self):
        self.target_number = random.randint(1, 100)
        self.attempts = 0
        self.attempts_label.config(text=f"Attempts left: {self.max_attempts}")
        self.guess_entry.delete(0, tk.END)

    def exit_fullscreen(self, event=None):
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        self.master.attributes('-fullscreen', False)
        self.master.geometry(f"{screen_width // 2}x{screen_height // 2}")
        self.master.configure(bg="#e0f7fa")

root = tk.Tk()
game = NumberGuessingGame(root)
root.mainloop()

