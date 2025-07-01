# PySearch - A Google-like Search Engine in Python

[![CI/CD Pipeline](https://github.com/shubhamphapale/search-engine-proto/actions/workflows/ci.yml/badge.svg)](https://github.com/shubhamphapale/search-engine-proto/actions/workflows/ci.yml)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://hub.docker.com/)
[![Flask](https://img.shields.io/badge/flask-3.1+-green.svg)](https://flask.palletsprojects.com/)

A fully functional search engine built in Python that mimics Google's core functionality including web crawling, indexing, ranking, and a web interface.

🔍 **[Live Demo](https://shubhamphapale.github.io/search-engine-proto/demo.html)** | 📖 **[Full Documentation](#documentation)** | 🚀 **[Deploy Now](#deployment)**

## Features

### 🔍 **Core Search Engine Features**
- **Web Crawling**: Automated web scraping with respectful crawling (delays, robots.txt respect)
- **Text Indexing**: TF-IDF based indexing with stemming and stopword removal
- **Ranking Algorithm**: Combines content relevance with simple PageRank-style scoring
- **Query Processing**: Advanced query preprocessing with spelling suggestions
- **Result Snippets**: Smart extraction of relevant text snippets with query highlighting

### 🌐 **Web Interface**
- **Google-like UI**: Clean, responsive design similar to Google's interface
- **Search Results**: Paginated results with relevance scores
- **Spelling Suggestions**: "Did you mean?" functionality for misspelled queries
- **Mobile Responsive**: Works on desktop and mobile devices

### 🛠 **Technical Features**
- **SQLite Database**: Efficient storage and retrieval of crawled pages
- **RESTful API**: JSON API endpoints for integration with other applications
- **Modular Architecture**: Separate components for crawling, indexing, and serving
- **Error Handling**: Robust error handling and logging

## Project Structure

```
search_engine/
├── main.py              # Main entry point and CLI
├── crawler.py           # Web crawler implementation
├── search_engine.py     # Core search and ranking logic
├── web_app.py          # Flask web application
├── requirements.txt     # Python dependencies
├── templates/
│   └── search.html     # Web interface template
├── database.db         # SQLite database (created after crawling)
└── README.md           # This file
```

## Installation & Setup

### 1. Install Dependencies

```bash
cd search_engine
pip install -r requirements.txt
```

### 2. Quick Start (Demo)

For a quick demo with pre-configured URLs:

```bash
python main.py
```

This will:
- Crawl sample websites (Wikipedia, Python docs, etc.)
- Build the search index
- Provide instructions to start the web server

### 3. Start the Web Server

```bash
python main.py server
```

Then visit `http://127.0.0.1:5000` in your browser.

## Usage

### Command Line Interface

#### Crawl Websites
```bash
# Crawl specific URLs
python main.py crawl https://example.com https://another-site.com

# Crawl with custom settings
python main.py crawl https://example.com --max-pages 100 --delay 1
```

#### Test Search Engine
```bash
python main.py test
```

#### Run Web Server
```bash
# Default settings (localhost:5000)
python main.py server

# Custom host and port
python main.py server --host 0.0.0.0 --port 8080

# Production mode (no debug)
python main.py server --no-debug
```

### API Endpoints

#### Search API
```bash
# Basic search
curl "http://localhost:5000/api/search?q=python+programming"

# Limit results
curl "http://localhost:5000/api/search?q=web+development&max_results=5"
```

#### Spelling Suggestions API
```bash
curl "http://localhost:5000/api/suggest?q=pythong"
```

### Python Integration

```python
from search_engine import SearchEngine

# Initialize search engine
engine = SearchEngine('database.db')

# Perform search
results = engine.search("python programming", max_results=10)

# Process results
for result in results:
    print(f"Title: {result['title']}")
    print(f"URL: {result['url']}")
    print(f"Score: {result['final_score']}")
    print(f"Snippet: {result['content_snippet']}")
    print("---")
```

## How It Works

### 1. Web Crawling
- **Respectful Crawling**: Includes delays between requests and respects robots.txt
- **Content Extraction**: Uses BeautifulSoup to parse HTML and extract text content
- **Link Discovery**: Follows links to discover new pages
- **Duplicate Prevention**: Tracks visited URLs to avoid crawling the same page twice

### 2. Indexing & Processing
- **Text Preprocessing**: Tokenization, stemming, and stopword removal using NLTK
- **TF-IDF Vectorization**: Creates numerical representations of documents using scikit-learn
- **Efficient Storage**: Stores processed content in SQLite database

### 3. Search & Ranking
- **Query Processing**: Applies same preprocessing to search queries
- **Similarity Calculation**: Uses cosine similarity between query and document vectors
- **PageRank-style Scoring**: Boosts authoritative domains and HTTPS sites
- **Result Ranking**: Combines content relevance with authority signals

### 4. Web Interface
- **Flask Backend**: Lightweight web framework for serving search results
- **Responsive Design**: HTML/CSS interface that works on all devices
- **Pagination**: Handles large result sets with page navigation
- **Real-time Search**: Fast response times through efficient indexing

## Architecture Details

### Database Schema
```sql
CREATE TABLE pages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT UNIQUE,
    title TEXT,
    content TEXT,
    keywords TEXT,
    crawl_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Key Algorithms

#### TF-IDF Scoring
- **Term Frequency**: How often a term appears in a document
- **Inverse Document Frequency**: How rare a term is across all documents
- **Combined Score**: TF × IDF gives relevance score for each term

#### PageRank-style Authority
- HTTPS sites get 10% boost
- Shorter URLs get 5% boost  
- Authoritative domains (Wikipedia, official docs) get 20% boost

#### Spelling Suggestions
- Edit distance algorithm to find similar words in vocabulary
- Suggests alternatives for misspelled query terms

## Deployment

### Quick Deploy to Cloud Platforms

This project includes configurations for one-click deployment to popular cloud platforms:

#### 🚀 **Render (Recommended - Free)**
1. Fork this repository
2. Connect your GitHub account to [Render](https://render.com)
3. Create a new "Web Service" from your forked repository
4. Render will automatically detect the `render.yaml` configuration
5. Your search engine will be live with pre-populated data!

#### 🚂 **Railway (Alternative - Free)**
1. Fork this repository  
2. Connect your GitHub account to [Railway](https://railway.app)
3. Deploy from your forked repository
4. Railway will use the `railway.json` configuration

#### ⚡ **Heroku (Paid)**
1. Fork this repository
2. Connect your Heroku account to GitHub
3. Create a new app and connect it to your forked repository
4. The `Procfile` will handle the deployment

### What Happens During Deployment

The `deploy.py` script automatically:
1. **Installs dependencies** from `requirements.txt`
2. **Crawls and indexes content** from popular programming sites:
   - Python documentation and Wikipedia
   - JavaScript, Machine Learning, Web Development topics
   - Algorithm and Computer Science resources
3. **Starts the web server** on the platform's assigned port
4. **Provides search functionality** immediately after deployment

### Local Development with Pre-populated Data

```bash
# Clone and setup
git clone https://github.com/ShubhamPhapale/search-engine-proto.git
cd search-engine-proto
pip install -r requirements.txt

# Initialize with sample data
python deploy.py
```

## Customization

### Adding New Ranking Factors
Edit the `calculate_page_rank()` method in `search_engine.py`:

```python
def calculate_page_rank(self, urls):
    scores = []
    for url in urls:
        score = 1.0
        
        # Add your custom ranking factors here
        if 'github.com' in url:
            score *= 1.3  # Boost GitHub repos
        
        if url.count('/') < 4:  # Homepage or top-level page
            score *= 1.1
            
        scores.append(score)
    return scores
```

### Customizing the Crawler
Modify `crawler.py` to:
- Respect robots.txt
- Add custom headers
- Filter specific content types
- Implement rate limiting per domain

### Extending the Web Interface
The HTML template in `templates/search.html` can be customized to:
- Change the design and branding
- Add filters and advanced search options
- Implement auto-complete functionality
- Add search analytics

## Performance Considerations

### For Large-Scale Deployment
- **Database**: Consider PostgreSQL for better performance with large datasets
- **Indexing**: Implement Elasticsearch for faster full-text search
- **Caching**: Add Redis for caching frequent queries
- **Load Balancing**: Use multiple server instances behind a load balancer

### Memory Usage
- Current implementation loads all documents into memory for TF-IDF
- For large corpora, consider incremental learning or external indexing

### Crawling Efficiency
- Implement parallel crawling with threading/async
- Add distributed crawling across multiple machines
- Implement smarter URL prioritization

## Known Limitations

1. **Scale**: Designed for thousands of pages, not millions like Google
2. **Ranking**: Simplified PageRank without link graph analysis
3. **Language**: Currently optimized for English content only
4. **Real-time**: Index updates require full rebuild
5. **Security**: No input sanitization for production use

## Future Enhancements

- [ ] Image search capability
- [ ] Real-time index updates
- [ ] Machine learning-based ranking
- [ ] Multi-language support
- [ ] Advanced query operators (site:, filetype:, etc.)
- [ ] Search analytics and user behavior tracking
- [ ] Distributed architecture for scalability

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Acknowledgments

- Inspired by Google's search architecture
- Built with Python's excellent ecosystem (Flask, scikit-learn, NLTK, BeautifulSoup)
- Thanks to the open source community for the foundational libraries
