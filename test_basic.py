#!/usr/bin/env python3
"""
Basic tests for the search engine functionality
"""

import os
import sqlite3
import sys
import tempfile
from crawler import WebCrawler
from search_engine import SearchEngine

def setup_test_database(db_path):
    """Setup a test database with sample data"""
    # Create crawler and setup database
    crawler = WebCrawler(db_path)
    crawler.setup_database()
    
    # Add test documents
    test_documents = [
        ("http://test1.com", "Python Programming Guide", 
         "Python is a powerful programming language used for web development, data science, and machine learning."),
        ("http://test2.com", "Web Development Tutorial", 
         "Learn web development with Flask, a lightweight Python web framework."),
        ("http://test3.com", "Machine Learning Basics", 
         "Machine learning is a subset of artificial intelligence that uses algorithms to analyze data.")
    ]
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    for url, title, content in test_documents:
        cursor.execute(
            'INSERT INTO pages (url, title, content) VALUES (?, ?, ?)',
            (url, title, content)
        )
    
    conn.commit()
    conn.close()
    
    print(f"Test database created with {len(test_documents)} documents")

def test_search_engine():
    """Test basic search engine functionality"""
    print("Running basic search engine tests...")
    
    # Create temporary database
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp_db:
        db_path = tmp_db.name
    
    try:
        # Setup test database
        setup_test_database(db_path)
        
        # Initialize search engine
        engine = SearchEngine(db_path)
        
        # Test 1: Check if documents are loaded
        assert len(engine.documents) > 0, "No documents loaded"
        print(f"✓ Documents loaded: {len(engine.documents)}")
        
        # Test 2: Test search functionality
        results = engine.search("python programming", max_results=5)
        assert len(results) > 0, "No search results found"
        print(f"✓ Search results found: {len(results)}")
        
        # Test 3: Test search with no results
        no_results = engine.search("nonexistent query xyz", max_results=5)
        print(f"✓ No results query handled: {len(no_results)} results")
        
        # Test 4: Test spelling suggestions
        suggestions = engine.suggest_spelling("pythong")
        print(f"✓ Spelling suggestions: {len(suggestions)} suggestions")
        
        print("All basic tests passed! ✅")
        return True
        
    except Exception as e:
        print(f"Test failed: {e}")
        return False
    
    finally:
        # Cleanup
        if os.path.exists(db_path):
            os.unlink(db_path)

def test_crawler():
    """Test basic crawler functionality"""
    print("Running basic crawler tests...")
    
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp_db:
        db_path = tmp_db.name
    
    try:
        # Test crawler initialization
        crawler = WebCrawler(db_path)
        
        # Test database setup
        crawler.setup_database()
        
        # Check if database was created properly
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='pages'")
        result = cursor.fetchone()
        conn.close()
        
        assert result is not None, "Database table not created"
        print("✓ Crawler database setup successful")
        
        print("Crawler tests passed! ✅")
        return True
        
    except Exception as e:
        print(f"Crawler test failed: {e}")
        return False
    
    finally:
        if os.path.exists(db_path):
            os.unlink(db_path)

def main():
    """Run all tests"""
    print("🔍 PySearch - Running Basic Tests")
    print("=" * 40)
    
    all_passed = True
    
    # Test crawler
    if not test_crawler():
        all_passed = False
    
    print()
    
    # Test search engine
    if not test_search_engine():
        all_passed = False
    
    print()
    print("=" * 40)
    
    if all_passed:
        print("🎉 All tests passed!")
        sys.exit(0)
    else:
        print("❌ Some tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
