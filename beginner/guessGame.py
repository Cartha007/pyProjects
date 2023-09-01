import random

def main():
    print("Starting the game.")
    try:
        print("What number range do you want to guess from? Enter them accordingly")
        a = int(input('>'))
        b = int(input('>'))
        randNumber = random.randint(a, b)
        guess = int(input('Guess the number: '))
        if guess == randNumber:
            print('You guessed right.')
        else:
            print('Wrong guess.')
    except Exception() as e:
        print(e)


if __name__ == "__main__":
    while True:
        main()
        if input("Repeat the program? (Y/N):").strip().upper() != "Y":
            break