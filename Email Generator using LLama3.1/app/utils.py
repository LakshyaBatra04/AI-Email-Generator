import re
from bs4 import BeautifulSoup

def clean_text(text):
    # Remove HTML tags
    text = re.sub(r'<.*?>', '', text)
    
    # Remove URLs (http://, https://, www, etc.)
    text = re.sub(r'http[s]?://\S+|www\.\S+', '', text)
    
    # Remove special characters, keeping spaces and alphanumeric characters
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

