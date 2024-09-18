import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Function to clean and normalize data
def preprocess_data(input_file, output_file):
    try:
        with open(input_file, 'r') as f:
            data = json.load(f)

        # Example preprocessing steps
        normalized_data = []
        for item in data['children']:
            normalized_item = {
                'title': item['title'],
                'url': item['url'],
                'description': item.get('description', '')
            }
            normalized_data.append(normalized_item)

        with open(output_file, 'w') as f:
            json.dump(normalized_data, f)

        logging.info(f"Data preprocessed and saved to {output_file}")
    except Exception as e:
        logging.error(f"Error preprocessing data: {e}")

# Main execution
if __name__ == "__main__":
    preprocess_data('khan_academy_data.json', 'preprocessed_khan_academy_data.json')
