import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import sqlite3
import time
import re

class WebCrawler:
    def __init__(self, db_path='database.db'):
        self.db_path = db_path
        self.visited_urls = set()
        self.setup_database()
    
    def setup_database(self):
        """Initialize the database schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT UNIQUE,
                title TEXT,
                content TEXT,
                keywords TEXT,
                crawl_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
    
    def get_page_content(self, url):
        """Fetch and parse a web page"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract title
            title = soup.find('title')
            title_text = title.get_text().strip() if title else ''
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Extract text content
            content = soup.get_text()
            # Clean up whitespace
            content = re.sub(r'\s+', ' ', content).strip()
            
            # Extract keywords from meta tags
            keywords = []
            meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
            if meta_keywords:
                keywords = [k.strip() for k in meta_keywords.get('content', '').split(',')]
            
            return title_text, content, keywords
            
        except Exception as e:
            print(f"Error crawling {url}: {e}")
            return None, None, None
    
    def store_page(self, url, title, content, keywords):
        """Store page data in the database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            keywords_str = ', '.join(keywords) if keywords else ''
            
            cursor.execute('''
                INSERT OR REPLACE INTO pages (url, title, content, keywords)
                VALUES (?, ?, ?, ?)
            ''', (url, title, content, keywords_str))
            
            conn.commit()
            conn.close()
            print(f"Stored: {url}")
            
        except Exception as e:
            print(f"Error storing {url}: {e}")
    
    def extract_links(self, soup, base_url):
        """Extract all links from a page"""
        links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(base_url, href)
            
            # Only include HTTP/HTTPS URLs
            if full_url.startswith(('http://', 'https://')):
                links.append(full_url)
        
        return links
    
    def crawl(self, start_urls, max_pages=100, delay=1):
        """Crawl web pages starting from given URLs"""
        urls_to_visit = list(start_urls)
        pages_crawled = 0
        
        while urls_to_visit and pages_crawled < max_pages:
            url = urls_to_visit.pop(0)
            
            if url in self.visited_urls:
                continue
            
            print(f"Crawling: {url}")
            self.visited_urls.add(url)
            
            title, content, keywords = self.get_page_content(url)
            
            if content:
                self.store_page(url, title, content, keywords)
                pages_crawled += 1
                
                # Extract links for further crawling
                try:
                    response = requests.get(url, timeout=10)
                    soup = BeautifulSoup(response.content, 'html.parser')
                    links = self.extract_links(soup, url)
                    
                    # Add new links to crawl queue
                    for link in links:
                        if link not in self.visited_urls:
                            urls_to_visit.append(link)
                            
                except Exception as e:
                    print(f"Error extracting links from {url}: {e}")
            
            # Be respectful - add delay between requests
            time.sleep(delay)
        
        print(f"Crawling completed. Crawled {pages_crawled} pages.")

if __name__ == "__main__":
    crawler = WebCrawler()
    
    # Example URLs to start crawling
    start_urls = [
        "https://en.wikipedia.org/wiki/Python_(programming_language)",
        "https://docs.python.org/3/",
        "https://realpython.com/"
    ]
    
    crawler.crawl(start_urls, max_pages=50, delay=2)
