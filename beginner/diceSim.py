import random

def rollDice():
    diceType = int(input("Enter the type of dice to roll: "))
    result = random.randint(1, diceType)
    print(f'You rolled a {result}')
    
    
if __name__ == "__main__":
    try:
        while True:
            user_input = input('Roll the dice? (Yes/No): ').lower()
            if user_input == 'yes':
                rollDice()
            else: break
    except KeyboardInterrupt:
        print('\nEnding the script.')