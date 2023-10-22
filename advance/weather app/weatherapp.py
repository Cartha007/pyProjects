from api_key import API_KEY
import requests, json

def get_weather(city, api_key):
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}'
    response = requests.get(url).text
    data = json.loads(response)
    # print(data)
    if data['cod'] != "404":
        m_data = data["main"]
        temperature = m_data["temp"]
        pressure = m_data["pressure"]
        humidity = m_data["humidity"]
        weather_data = data["weather"][0]
        description = weather_data["description"]
        
        temp_celcius = temperature - 273.15
        
        print(f"Weather in {city}:")
        print(f"Temperature: {temp_celcius:.2f}°C")
        print(f"Pressure: {pressure} hPa")
        print(f"Humidity: {humidity}%")
        print(f"Description: {description.capitalize()}")
    else:
        print("City not found")


if __name__ == "__main__":
    api_key = API_KEY
    print("Enter city name: ")
    city_name = input('>')
    get_weather(city_name, api_key)