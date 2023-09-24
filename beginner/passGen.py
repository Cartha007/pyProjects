import random
import string

def generate_password(length, add_upper, add_lower, add_numbers, add_special_char):
    characters = ""
    if add_upper:
        characters += string.ascii_uppercase
    if add_lower:
        characters += string.ascii_lowercase
    if add_numbers:
        characters += string.digits
    if add_special_char:
        characters += string.punctuation
    
    if not characters:
        print("Please select at least one option.")
        return None
    password = "".join(random.choice(characters) for _ in range(length))
    return password

def main():    
    length = int(input("Enter the length of the password: "))
    add_upper = input("Include uppercase letters? (y/n): ").lower() == 'y'
    add_lower = input("Include lowercase letters? (y/n): ").lower() == 'y'
    add_numbers = input("Include numbers? (y/n): ").lower() == 'y'
    add_special_char = input("Include special characters? (y/n): ").lower() == 'y'
    
    password = generate_password(length, add_upper, add_lower, add_numbers, add_special_char)
    if password:
        print(f"Your generated password is: {password}")


if __name__ == "__main__":
    main()