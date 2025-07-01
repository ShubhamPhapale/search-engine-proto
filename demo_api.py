#!/usr/bin/env python3
"""
Quick demo script to show the search engine API functionality
"""

from search_engine import SearchEngine
import json

def demo_search_engine():
    """Demonstrate the search engine capabilities"""
    print("🔍 PySearch - Google-like Search Engine Demo")
    print("=" * 50)
    
    # Initialize search engine
    engine = SearchEngine('database.db')
    
    # Demo queries
    demo_queries = [
        "python programming",
        "web development", 
        "machine learning",
        "flask framework",
        "wikipedia"
    ]
    
    for query in demo_queries:
        print(f"\n🔎 Searching for: '{query}'")
        print("-" * 40)
        
        results = engine.search(query, max_results=3)
        
        if results:
            for i, result in enumerate(results, 1):
                print(f"\n{i}. {result['title'][:60]}...")
                print(f"   🌐 URL: {result['url']}")
                print(f"   📊 Relevance Score: {result['final_score']:.4f}")
                print(f"   📝 Snippet: {result['content_snippet'][:100]}...")
        else:
            print("   ❌ No results found")
    
    # Demo spelling suggestions
    print(f"\n🔤 Spelling Suggestions Demo")
    print("-" * 40)
    
    misspelled_queries = ["pythong", "develoment", "lerning"]
    for query in misspelled_queries:
        suggestions = engine.suggest_spelling(query)
        print(f"'{query}' → {suggestions}")

if __name__ == "__main__":
    demo_search_engine()
