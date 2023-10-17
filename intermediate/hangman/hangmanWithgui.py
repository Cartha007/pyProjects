import random
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from someWordList import words  # Import the word list from someWordList module

# Function to display the hangman figure based on the number of mistakes
def hangman(mistakes: int):
    # Hangman art representation
    art = [
        "\n+---+\n O   |\n/|\  |\n/ \  |\n    ===",
        "\n+---+\n O  |\n/|\ |\n/   |\n   ===",
        "\n+---+\n O  |\n/|\ |\n    |\n   ===",
        "\n+---+\n O  |\n/|  |\n    |\n   ===",
        "\n+---+\nO   |\n|   |\n    |\n   ===",
        "\n+---+\nO   |\n    |\n    |\n   ===",
        "\n+---+\n    |\n    |\n    |\n   ===",
        "\n+---+\n    |\n    |\n    |\n   ===",
    ]
    # Update the hangman_label with the hangman art
    hangman_label.config(text=art[mistakes])

# Function to display the current state of the word
def display_word(word, guesses):
    displayed_word = ""
    for letter in word:
        if letter.lower() in guesses:
            displayed_word += letter + " "
        else:
            displayed_word += "_ "
    return displayed_word

# Function to close the game with a confirmation dialog
def close_game():
    response = messagebox.askyesno('Alert', 'Do you want to exit the game?')
    if response == True:
        root.destroy()

# Create the main tkinter window
root = Tk()
# Create a label for displaying the hangman figure
hangman_label = tk.Label(root, font=('CourierK', 16))

# Main game logic
def main():
    print("<===== Hangman game =====>")
    
    # Tkinter setup
    root.geometry("250x280")
    root.title("Hangman")
    root.config(bg='#E7FFFF')
    
    hangman_label.grid(row=0, column=0)
    
    word = random.choice(words)  # Choose a random word from the word list
    errors_allowed = 7
    guesses = []

    word_label = tk.Label(root, text=display_word(word, guesses), font=("Arial", 24), bg='#E7FFFF')
    word_label.grid(row=1, column=0)

    # Function to make a guess
    hangman(errors_allowed)
    def make_guess():
        nonlocal errors_allowed
        guess = guess_entry.get().lower()
        guesses.append(guess)
        guess_entry.delete(0, 'end')
        if guess not in word.lower():
            errors_allowed -= 1
        word_label.config(text=display_word(word, guesses))
        hangman(errors_allowed)
        if errors_allowed == 0:
            end_game(False)
        elif all(letter.lower() in guesses for letter in word):
            end_game(True)

    # Create an entry for guessing and a button for making a guess
    guess_entry = tk.Entry(root, width=3, font=("Arial", 24))
    guess_entry.grid(row=2, column=0)
    guess_button = tk.Button(root, text="Guess", command=make_guess)
    guess_button.grid(row=2, column=1)

    # Function to end the game
    def end_game(is_winner):
        if is_winner:
            messagebox.showinfo("Game Over", f"You have found the word! It was {word}!")
        else:
            messagebox.showinfo("Game Over", f"Game over! The word was {word}!")
        response = messagebox.askyesno('Alert', 'Do you want to play again?')
        if response == False:
            root.destroy()
        main()

    root.protocol("WM_DELETE_WINDOW", close_game)  # Handle window close button

if __name__ == "__main__":
    main()
    root.mainloop()  # Start the tkinter event loop
