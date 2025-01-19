import requests

url = "https://api.jsonserve.com/rJvd7g"

response = requests.get(url)

if response.status_code == 200:
    print("Fetched Data:")
    print(response.json())  # Print the JSON response
else:
    print(f"Error: {response.status_code}")
