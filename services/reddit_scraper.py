
import os
import requests
import logging
from typing import List, Dict, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RedditMemeAPI:
    def __init__(self):
        self.client_id = os.getenv('REDDIT_CLIENT_ID')
        self.client_secret = os.getenv('REDDIT_CLIENT_SECRET')
        self.user_agent = os.getenv('REDDIT_USER_AGENT', 'WeatherApp/1.0')
        self.access_token = None
        
    def get_auth_token(self) -> Optional[str]:
        """Get Reddit API authentication token"""
        try:
            auth = requests.auth.HTTPBasicAuth(self.client_id, self.client_secret)
            data = {
                'grant_type': 'client_credentials',
            }
            headers = {
                'User-Agent': self.user_agent
            }
            response = requests.post(
                'https://www.reddit.com/api/v1/access_token',
                auth=auth,
                data=data,
                headers=headers
            )
            self.access_token = response.json()['access_token']
            return self.access_token
        except Exception as e:
            logger.error(f"Error getting Reddit auth token: {str(e)}")
            return None

    def get_weather_memes(self, subreddit: str = 'weathermemes', limit: int = 10) -> List[Dict]:
        """Get weather-related memes from Reddit
        
        Args:
            subreddit (str): Subreddit to fetch memes from
            limit (int): Number of memes to fetch
            
        Returns:
            List[Dict]: List of meme dictionaries with url and title
        """
        if not self.access_token:
            self.get_auth_token()
            
        if not self.access_token:
            logger.error("Failed to get access token")
            return []
            
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'User-Agent': self.user_agent
        }
        
        try:
            response = requests.get(
                f'https://oauth.reddit.com/r/{subreddit}/hot',
                headers=headers,
                params={'limit': limit}
            )
            
            if response.status_code != 200:
                logger.error(f"Reddit API error: {response.status_code}")
                return []
                
            posts = response.json()['data']['children']
            memes = []
            
            for post in posts:
                data = post['data']
                if data.get('post_hint') == 'image' or any(data['url'].endswith(ext) for ext in ['.jpg', '.png', '.gif']):
                    meme = {
                        'url': data['url'],
                        'title': data['title'],
                        'subreddit': data['subreddit'],
                        'score': data['score'],
                        'author': data['author']
                    }
                    memes.append(meme)
                    
            return memes
            
        except Exception as e:
            logger.error(f"Error fetching memes: {str(e)}")
            return []

# Create singleton instance
reddit_api = RedditMemeAPI()
