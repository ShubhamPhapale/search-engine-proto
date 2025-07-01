#!/usr/bin/env python3
"""
PySearch - A Google-like Search Engine in Python

This is the main entry point for the search engine.
It provides options to crawl websites, build the index, and run the web server.
"""

import argparse
import sys
import os
from crawler import WebCrawler
from search_engine import SearchEngine
from web_app import app, initialize_search_engine

def crawl_websites(urls, max_pages=50, delay=2):
    """Crawl websites and populate the database"""
    print(f"Starting to crawl {len(urls)} websites...")
    print(f"Max pages: {max_pages}, Delay: {delay} seconds")
    
    crawler = WebCrawler('database.db')
    crawler.crawl(urls, max_pages=max_pages, delay=delay)
    
    print("Crawling completed!")

def test_search_engine():
    """Test the search engine with sample queries"""
    print("Testing search engine...")
    
    engine = SearchEngine('database.db')
    
    # Check if we have any documents to search
    if not engine.documents:
        print("No documents found in database. Running setup first...")
        # Run setup to populate database
        setup_demo()
        # Reinitialize engine
        engine = SearchEngine('database.db')
        
        if not engine.documents:
            print("Still no documents found. Cannot run tests.")
            return
    
    test_queries = [
        "python programming",
        "web development",
        "machine learning",
        "data science",
        "flask framework"
    ]
    
    for query in test_queries:
        print(f"\n--- Searching for: '{query}' ---")
        results = engine.search(query, max_results=3)
        
        if results:
            for i, result in enumerate(results, 1):
                print(f"{i}. {result['title'][:60]}...")
                print(f"   URL: {result['url']}")
                print(f"   Score: {result['final_score']:.4f}")
        else:
            print("No results found.")

def run_web_server(host='127.0.0.1', port=5000, debug=True):
    """Run the Flask web server"""
    print(f"Starting web server at http://{host}:{port}")
    print("Press Ctrl+C to stop the server")
    
    # Initialize the search engine
    initialize_search_engine()
    
    app.run(host=host, port=port, debug=debug)

def main():
    parser = argparse.ArgumentParser(description='PySearch - A Google-like Search Engine')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Crawl command
    crawl_parser = subparsers.add_parser('crawl', help='Crawl websites and build index')
    crawl_parser.add_argument('urls', nargs='+', help='URLs to start crawling from')
    crawl_parser.add_argument('--max-pages', type=int, default=50, 
                             help='Maximum number of pages to crawl (default: 50)')
    crawl_parser.add_argument('--delay', type=float, default=2, 
                             help='Delay between requests in seconds (default: 2)')
    
    # Test command
    test_parser = subparsers.add_parser('test', help='Test the search engine')
    
    # Server command
    server_parser = subparsers.add_parser('server', help='Run the web server')
    server_parser.add_argument('--host', default='127.0.0.1', 
                              help='Host to bind to (default: 127.0.0.1)')
    server_parser.add_argument('--port', type=int, default=5000, 
                              help='Port to bind to (default: 5000)')
    server_parser.add_argument('--no-debug', action='store_true', 
                              help='Disable debug mode')
    
    # Parse arguments
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Execute commands
    if args.command == 'crawl':
        crawl_websites(args.urls, args.max_pages, args.delay)
    
    elif args.command == 'test':
        test_search_engine()
    
    elif args.command == 'server':
        run_web_server(args.host, args.port, not args.no_debug)

def setup_demo():
    """Set up a demo with sample data"""
    print("Setting up demo with sample URLs...")
    
    demo_urls = [
        "https://en.wikipedia.org/wiki/Python_(programming_language)",
        "https://docs.python.org/3/tutorial/",
        "https://realpython.com/python-basics/",
        "https://www.python.org/about/",
        "https://en.wikipedia.org/wiki/Web_development",
        "https://flask.palletsprojects.com/en/2.3.x/",
        "https://en.wikipedia.org/wiki/Machine_learning"
    ]
    
    # Check if database exists and has data
    if os.path.exists('database.db'):
        import sqlite3
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM pages")
        count = cursor.fetchone()[0]
        conn.close()
        
        if count > 0:
            print(f"Database already has {count} pages. Skipping crawl.")
            print("Run 'python main.py server' to start the web interface.")
            return
    
    print("Crawling demo websites...")
    crawl_websites(demo_urls, max_pages=20, delay=1)
    
    print("\nDemo setup complete!")
    print("You can now:")
    print("1. Test search: python main.py test")
    print("2. Start web server: python main.py server")
    print("3. Visit http://127.0.0.1:5000 in your browser")

if __name__ == '__main__':
    # If no arguments provided, set up demo
    if len(sys.argv) == 1:
        setup_demo()
    else:
        main()
