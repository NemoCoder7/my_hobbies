import requests
from requests import HTTPError

response = requests.get("https://www.youtube.com")

print(type(response))

for url in ["https://www.youtube.com", "https://www.yout.com"]:
    try:
        response = requests.get(url)
        
        response.raise_for_status()
    except HTTPError as http_err:
        print('error')
    except Exception as err:
        print('unknown error')
    else:
        print("Connected seccessfully")
        
print(response.content)