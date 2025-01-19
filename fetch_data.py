import requests
import pandas as pd

# API URL
API_URL = "https://api.jsonserve.com/XgAgFJ"

try:
    # Fetch data
    response = requests.get(API_URL)

    if response.status_code == 200:
        data = response.json()  # Convert JSON to Python dictionary

        # Convert data to DataFrame
        df = pd.DataFrame(data)

        # Save to CSV
        df.to_csv("student_quiz_performance.csv", index=False)

        print("✅ Data successfully fetched and saved as student_quiz_performance.csv")
    else:
        print(f"❌ Failed to fetch data. Status Code: {response.status_code}")

except Exception as e:
    print(f"❌ Error: {e}")
