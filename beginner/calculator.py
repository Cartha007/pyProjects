def calculator():
    print("Please select one:")
    operation = input("Division(D), Multiplication(M), Addition(A), Subtraction(S)")
    operation = operation.strip()[0].upper()
    
    operations = {
        "D": lambda x,y: x/y,
        "M": lambda x,y: x*y,
        "A": lambda x,y: x+y,
        "S": lambda x,y: x-y
    }
    
    if operation not in operations:
        print("Invalid option")
        return
    
    num1 = input("Enter number: ")
    if not num1.isnumeric():
        print("Invalid input.")
        return
    num2 = input("Enter second number: ")
    if not num2.isnumeric():
        print("Invalid input.")
        return
    
    # Perform the operation and print the result
    ans = operations[operation](float(num1), float(num2))
    print(f'{num1} {operation} {num2} = {ans}')
    
    
if __name__ == "__main__":
    while True:
        calculator()
        if input('Repeat the program? (Y/N):').strip().upper() != "Y":
            break