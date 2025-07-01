#!/bin/bash

echo "PySearch - Starting deployment initialization..."

# Check if database exists, if not, populate it
if [ ! -f "search_engine.db" ]; then
    echo "No existing database found. Starting data crawling and indexing..."
    
    # Crawl and index popular programming topics
    python main.py crawl --url https://en.wikipedia.org/wiki/Python_(programming_language) --depth 2
    python main.py crawl --url https://en.wikipedia.org/wiki/JavaScript --depth 1
    python main.py crawl --url https://en.wikipedia.org/wiki/Machine_learning --depth 1
    python main.py crawl --url https://en.wikipedia.org/wiki/Web_development --depth 1
    python main.py crawl --url https://en.wikipedia.org/wiki/Algorithm --depth 1
    python main.py crawl --url https://docs.python.org/3/tutorial/ --depth 1
    
    echo "Data indexing completed!"
else
    echo "Existing database found. Skipping data crawling."
fi

echo "Starting PySearch server..."
python main.py server --port ${PORT:-8080} --host ${HOST:-0.0.0.0}
