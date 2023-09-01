import random
from someWordList import words

# Prints hangman, got it from Shaun Halverson
def hangman(incorrect):
    if incorrect == 6:
        print("\n+---+")
        print("    |")
        print("    |")
        print("    |")
        print("   ===")
    elif incorrect == 5:
        print("\n+---+")
        print("O   |")
        print("    |")
        print("    |")
        print("   ===")
    elif incorrect == 4:
        print("\n+---+")
        print("O   |")
        print("|   |")
        print("    |")
        print("   ===")
    elif incorrect == 3:
        print("\n+---+")
        print(" O  |")
        print("/|  |")
        print("    |")
        print("   ===")
    elif incorrect == 2:
        print("\n+---+")
        print(" O  |")
        print("/|\ |")
        print("    |")
        print("   ===")
    elif incorrect == 1:
        print("\n+---+")
        print(" O  |")
        print("/|\ |")
        print("/   |")
        print("   ===")
    elif incorrect == 0:
        print("\n+---+")
        print(" O   |")
        print("/|\  |")
        print("/ \  |")
        print("    ===")

def main():
    print("<===== Hangman game =====>")
    print("Use Ctrl + c to end the game.")
    word = random.choice(words)
    errors_allowed = 7
    guesses = []
    done = False

    while not done:
        for letter in word:
            if letter.lower() in guesses:
                print(letter, end=" ")
            else:
                print("_", end=" ")
        print("")
        
        guess = input(f"Allowed erros left {errors_allowed}, Next Guess: ")
        guesses.append(guess.lower())
        if guess.lower() not in word.lower():
            errors_allowed -= 1
            if errors_allowed == 0:
                break
        
        hangman(errors_allowed)
        
        done = True
        for letter in word:
            if letter.lower() not in guesses:
                done = False
                
    if done:
        print(f"You have found the word! It was {word}!")
    else:
        hangman(errors_allowed)
        print(f"Game over! The word was {word}!")
        
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nEnding the game.")