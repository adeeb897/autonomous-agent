import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SocialMediaAPI:
    def __init__(self, ayrshare_api_key):
        self.ayrshare_api_key = ayrshare_api_key

    def post_to_social_media(self, content, platforms=['twitter', 'facebook']):
        url = "https://app.ayrshare.com/api/post"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.ayrshare_api_key}"
        }
        data = {
            "post": content,
            "platforms": platforms
        }
        try:
            response = requests.post(url, json=data, headers=headers)
            if response.status_code == 200:
                logger.info(f"Social Media Post successful: {response.json()}")
            else:
                logger.error(f"Social Media Post failed: {response.status_code}, {response.text}")
        except Exception as e:
            logger.error(f"Error posting to social media: {e}")
