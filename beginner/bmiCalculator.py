
def calcBmi(weight: float, height: float) -> float:
    try:
        if weight <= 0 or height <=0:
            raise ValueError("Weight and height must be positive numbers.")
        
        bmi = weight/ (height ** 2)
        return bmi
    except ValueError as e:
        return str(e)

def interpretBmi(bmi) -> str:
    if isinstance(bmi, str):
        return bmi
    elif bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal Weight"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obese"

def main():
    print("===== BMI Calculator =====")
    try:
        while True:
            weight = float(input("Enter your weight(kg): "))
            height = float(input("Enter your height(m): "))
            
            bmi = calcBmi(weight, height)
            interpretation = interpretBmi(bmi)
            
            if isinstance(bmi, str):
                print(f"Error: {bmi}")
            else:
                print(f"Your BMI is {bmi}. You are {interpretation}")
            response = input("Rerun? (Y/N): ").lower()
            if response != 'y':
                print("Quiting...")
                break
    except ValueError:
        print("Invalid Character!")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nEnding Script.")