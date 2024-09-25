import requests
import os

class AyrshareAPI:
    def __init__(self):
        self.api_key = os.getenv('AYRSHARE_API_KEY')
        self.base_url = 'https://app.ayrshare.com/api/'

    def post_social_media(self, content):
        url = self.base_url + 'post'
        headers = {'Authorization': f'Bearer {self.api_key}', 'Content-Type': 'application/json'}
        data = {
            'post': content,
            'platforms': ['twitter', 'facebook', 'linkedin']
        }

        try:
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 200:
                print(f"Post successful: {response.json()}")
            else:
                print(f"Failed to post: {response.status_code}, {response.text}")
        except Exception as e:
            print(f"Error posting to social media: {e}")

# Usage example
# ayrshare_api = AyrshareAPI()
# ayrshare_api.post_social_media("Hello, this is a test post!")
