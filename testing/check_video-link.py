import requests
from bs4 import BeautifulSoup

def is_valid_youtube_video(url):
    try:
        # Send a request to the YouTube page
        response = requests.get(url)
        if response.status_code != 200:
            return False

        # Parse the HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Look for the 'unavailable' message in the HTML
        if "Video unavailable" in soup.text:
            return False
            
        return True
    except Exception as e:
        return False

# Example Usage
url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
print(is_valid_youtube_video(url))
