import requests
from bs4 import BeautifulSoup

# Read the list of sources from data_sources.md
with open('data_sources.md', 'r') as file:
    sources = file.readlines()

# Filter out the URLs from the sources list
urls = [line.split(': ')[1].strip() for line in sources if line.startswith('1.') or line.startswith('2.') or line.startswith('3.') or line.startswith('4.') or line.startswith('5.') or line.startswith('6.')]

# Function to fetch data from a URL
def fetch_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return None

# Fetch data from each URL and save it
for url in urls:
    data = fetch_data(url)
    if data:
        # Parse the data using BeautifulSoup
        soup = BeautifulSoup(data, 'html.parser')
        # Save the parsed data to a file
        filename = url.split('//')[1].replace('/', '_') + '.html'
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(soup.prettify())
        print(f"Data from {url} saved to {filename}")
