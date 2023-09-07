import requests

'''
You would need an open exchange rates account for an app_id
'''

def convert_currency():
    pass

def main():
    app_id = "Your_App_Id"
    
    url = f"https://openexchangerates.org/api/latest.json?app_id={app_id}"
    response = requests.get(url)
    data = response.json()
    print(data)

if __name__ == "__main__":
    main()