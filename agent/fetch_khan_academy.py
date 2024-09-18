import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Function to fetch data from Khan Academy
def fetch_khan_academy_data():
    url = "https://www.khanacademy.org/api/v1/topictree"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        logging.info("Data fetched successfully from Khan Academy")
        return data
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data: {e}")
        return None

# Main execution
if __name__ == "__main__":
    data = fetch_khan_academy_data()
    if data:
        # Process the data or save to a file for further processing
        with open("khan_academy_data.json", "w") as f:
            json.dump(data, f)
        logging.info("Data saved to khan_academy_data.json")
