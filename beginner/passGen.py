import random

def main():
    uppercase_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    lowercase_letters ='abcdefghijklmnopqrstuvwxyz'
    numbers = '0123456789'
    special_characters = '!@#$%^&*()_+-=[]{}|;:,.<>?'
    
    length = int(input("Enter the length of the password: "))
    add_upper = input("Include uppercase letters? (y/n): ").lower() == 'y'
    add_lower = input("Include lowercase letters? (y/n): ").lower() == 'y'
    add_numbers = input("Include numbers? (y/n): ").lower() == 'y'
    add_special_char = input("Include special characters? (y/n): ").lower() == 'y'
    
    characters = ""
    if add_upper:
        characters += uppercase_letters
    if add_lower:
        characters += lowercase_letters
    if add_numbers:
        characters += numbers
    if add_special_char:
        characters += special_characters
    password = "".join(random.choice(characters) for _ in range(length))
    
    print(f"Your generated password is: {password}")


if __name__ == "__main__":
    main()