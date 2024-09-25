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
                log_social_media_post(content)
            else:
                print(f"Failed to post: {response.status_code}, {response.text}")
        except Exception as e:
            print(f"Error posting to social media: {e}")

def log_social_media_post(content):
    # A function to log the social media post details
    with open("social_media_log.txt", "a") as log_file:
        log_file.write(f"Content: {content}\n")

def post_social_media(content):
    ayrshare_api = AyrshareAPI()
    ayrshare_api.post_social_media(content)
