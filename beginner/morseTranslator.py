morse_code_dict = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 
    'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.', 
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...', 
    '8': '---..', '9': '----.',
    ' ': '/'
}

def english_to_morse(text):
    pass

def morse_to_english(text):
    pass

def options():
    print('(1) English to Morse code.\n(2) Morse code to English.\n(3) Quit.')

def main():
    print("---- Morse Code Translator ----")
    while True:
        options()
        response = int(input('> '))
        if response == 1:
            text = input("Enter text to convert to morse: ")
            morseCode = english_to_morse(text)
            print(f"Morse code: {morseCode}")
        elif response == 2:
            morseCode = input("Enter Morse code to convert to English: ")
            text = morse_to_english(morseCode)
            print(f"English: {text}")
        elif response == 3:
            print('Quitting...')
            break
        else:
            print("Invalid option. Please select a valid option.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nEnding script...")
    except ValueError:
        print("Error: Invalid character!")
    except Exception as e:
        print(f'Error: {e}')