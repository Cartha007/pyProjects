from playsound import playsound # Pip install --upgrade wheel playsound
import winsound # Only windows users
import time

# English letter to Morse code dictionary
morseCodeDict = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 
    'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.', 
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...', 
    '8': '---..', '9': '----.',
    ' ': '/'
}

# Morse code to English letter dictionary
englishDict = {v: k for k,v in morseCodeDict.items()}

def english_to_morse(text):
    morseCode = ''
    for char in text.upper():
        if char in morseCodeDict:
            morseCode += morseCodeDict[char] + ' '
        else:
            morseCode += char + ' '
    return morseCode

def morse_to_english(morseCode):
    morse = [code for code in morseCode.split(" ")]
    english = ''
    for char in morse:
        if char in englishDict:
            english += englishDict[char]
        else:
            english += char
    return english

def playMorse(morseCode):
    for char in morseCode:
        if char == ".":
            # playsound("short.mp3")
            winsound.Beep(1000, 200)
            time.sleep(0.1)
        elif char == "-":
            # playsound("long.mp3")
            winsound.Beep(1000, 500)
            time.sleep(0.1)
        elif char == "/" or char == " ":
            time.sleep(0.3)
        else:
            print("Invalid character.")

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
            # playMorse(morseCode) # Don't have the audios yet
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