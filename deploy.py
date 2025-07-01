#!/usr/bin/env python3
"""
Deployment initialization script for PySearch
Handles data crawling and server startup for cloud platforms
"""

import os
import sys
import subprocess
import time

def log(message):
    """Print timestamped log message"""
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {message}")

def run_command(command):
    """Run a command and return success status"""
    try:
        log(f"Running: {' '.join(command)}")
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        log(f"Error running command: {e}")
        if e.stderr:
            print(f"Error output: {e.stderr}")
        return False

def initialize_data():
    """Initialize search engine data by crawling popular sites"""
    log("PySearch - Starting deployment initialization...")
    
    # Check if database exists
    if os.path.exists("search_engine.db"):
        log("Existing database found. Skipping data crawling.")
        return True
    
    log("No existing database found. Starting data crawling and indexing...")
    
    # List of URLs to crawl with their depths
    crawl_targets = [
        ("https://en.wikipedia.org/wiki/Python_(programming_language)", 2),
        ("https://en.wikipedia.org/wiki/JavaScript", 1),
        ("https://en.wikipedia.org/wiki/Machine_learning", 1),
        ("https://en.wikipedia.org/wiki/Web_development", 1),
        ("https://en.wikipedia.org/wiki/Algorithm", 1),
        ("https://docs.python.org/3/tutorial/", 1),
    ]
    
    success_count = 0
    for url, depth in crawl_targets:
        log(f"Crawling {url} (depth: {depth})")
        if run_command(["python", "main.py", "crawl", "--url", url, "--depth", str(depth)]):
            success_count += 1
        else:
            log(f"Failed to crawl {url}, continuing...")
    
    if success_count > 0:
        log(f"Data indexing completed! Successfully crawled {success_count}/{len(crawl_targets)} targets.")
        return True
    else:
        log("Warning: No sites were successfully crawled. Starting with empty database.")
        return False

def start_server():
    """Start the search engine server"""
    port = os.environ.get('PORT', '8080')
    host = os.environ.get('HOST', '0.0.0.0')
    
    log(f"Starting PySearch server on {host}:{port}")
    
    # Start the server
    try:
        subprocess.run(["python", "main.py", "server", "--port", port, "--host", host], check=True)
    except subprocess.CalledProcessError as e:
        log(f"Failed to start server: {e}")
        sys.exit(1)

def main():
    """Main deployment function"""
    try:
        # Initialize data
        initialize_data()
        
        # Start server
        start_server()
        
    except KeyboardInterrupt:
        log("Deployment interrupted by user")
        sys.exit(0)
    except Exception as e:
        log(f"Deployment failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
