class UnitConverter:
    def __init__(self):
        self.conversions = {
            "length": {
                "meters_to_kilometers": lambda x: x / 1000,
                "kilometers_to_meters": lambda x: x * 1000,
                "meters_to_centimeters": lambda x: x * 100,
                "centimeters_to_meters": lambda x: x / 100,
                "inches_to_centimeters": lambda x: x * 2.54,
                "centimeters_to_inches": lambda x: x / 2.54,
                "feet_to_meters": lambda x: x * 0.3048,
                "meters_to_feet": lambda x: x / 0.3048,
            },
            "mass": {
                "grams_to_kilograms": lambda x: x / 1000,
                "kilograms_to_grams": lambda x: x * 1000,
                "pounds_to_kilograms": lambda x: x * 0.453592,
                "kilograms_to_pounds": lambda x: x / 0.453592,
            },
            "temperature": {
                "celsius_to_fahrenheit": lambda x: (x * 9/5) + 32,
                "fahrenheit_to_celsius": lambda x: (x - 32) * 5/9,
                "celsius_to_kelvin": lambda x: x + 273.15,
                "kelvin_to_celsius": lambda x: x - 273.15,
                "fahrenheit_to_kelvin": lambda x: (x - 32) * 5/9 + 273.15,
                "kelvin_to_fahrenheit": lambda x: (x - 273.15) * 9/5 + 32,
            },
            "volume": {
                "liters_to_milliliters": lambda x: x * 1000,
                "milliliters_to_liters": lambda x: x / 1000,
                "gallons_to_liters": lambda x: x * 3.78541,
                "liters_to_gallons": lambda x: x / 3.78541,
            },
            "time": {
                "seconds_to_minutes": lambda x: x / 60,
                "minutes_to_seconds": lambda x: x * 60,
                "hours_to_minutes": lambda x: x * 60,
                "minutes_to_hours": lambda x: x / 60,
            }
        }

    def display_conversions(self):
        print("Available conversions:")
        for category, conversions in self.conversions.items():
            print(f"\nCategory: {category.capitalize()}")
            for conversion in conversions.keys():
                print(f"  - {conversion}")

    def convert(self, category, conversion, value):
        try:
            result = self.conversions[category][conversion](value)
            return f"{value} {conversion.replace('_', ' ')} = {result}"
        except KeyError:
            return "Conversion not found. Please check your category and conversion type."


if __name__ == "__main__":
    converter = UnitConverter()
    
    # Display available conversions
    converter.display_conversions()
    
    # Get user input
    category = input("\nEnter the category (length, mass, temperature, volume, time): ").strip().lower()
    conversion = input("Enter the conversion (e.g., meters_to_kilometers): ").strip().lower()
    value = float(input("Enter the value to be converted: "))

    # Perform conversion and display the result
    result = converter.convert(category, conversion, value)
    print(result)
