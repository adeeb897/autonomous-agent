import requests

# Function to fetch data from a given URL
def fetch_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None

# Example usage
if __name__ == "__main__":
    url = "https://example.com/data"
    data = fetch_data(url)
    if data:
        print("Data fetched successfully")
    else:
        print("Failed to fetch data")