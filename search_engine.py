import sqlite3
import re
import math
from collections import defaultdict, Counter
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

class SearchEngine:
    def __init__(self, db_path='database.db'):
        self.db_path = db_path
        self.stemmer = PorterStemmer()
        self.stop_words = set(stopwords.words('english'))
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=10000,
            stop_words='english',
            lowercase=True,
            ngram_range=(1, 2)
        )
        self.documents = []
        self.document_urls = []
        self.document_titles = []
        self.tfidf_matrix = None
        self.load_documents()
        self.build_index()
    
    def load_documents(self):
        """Load documents from database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Check if table exists
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='pages'")
            if not cursor.fetchone():
                print("No database found. Run crawler first to populate database.")
                conn.close()
                return
            
            cursor.execute("SELECT url, title, content FROM pages")
            results = cursor.fetchall()
            conn.close()
            
            for url, title, content in results:
                self.document_urls.append(url)
                self.document_titles.append(title or "")
                self.documents.append(content or "")
                
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        except Exception as e:
            print(f"Error loading documents: {e}")
    
    def preprocess_text(self, text):
        """Clean and preprocess text"""
        # Convert to lowercase and remove special characters
        text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text.lower())
        
        # Tokenize
        tokens = word_tokenize(text)
        
        # Remove stopwords and stem
        processed_tokens = []
        for token in tokens:
            if token not in self.stop_words and len(token) > 2:
                stemmed = self.stemmer.stem(token)
                processed_tokens.append(stemmed)
        
        return ' '.join(processed_tokens)
    
    def build_index(self):
        """Build TF-IDF index for all documents"""
        if not self.documents:
            print("No documents found in database")
            return
        
        # Preprocess all documents
        processed_docs = [self.preprocess_text(doc) for doc in self.documents]
        
        # Build TF-IDF matrix
        self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(processed_docs)
        print(f"Index built for {len(self.documents)} documents")
    
    def calculate_page_rank(self, urls):
        """Simple page rank calculation based on URL characteristics"""
        scores = []
        for url in urls:
            score = 1.0
            
            # Boost for HTTPS
            if url.startswith('https://'):
                score *= 1.1
            
            # Boost for shorter URLs (more authoritative)
            if len(url) < 50:
                score *= 1.05
            
            # Boost for certain domains
            authoritative_domains = ['wikipedia.org', 'docs.python.org', 'stackoverflow.com']
            for domain in authoritative_domains:
                if domain in url:
                    score *= 1.2
                    break
            
            scores.append(score)
        
        return scores
    
    def search(self, query, max_results=10):
        """Search for documents matching the query"""
        if not self.documents or self.tfidf_matrix is None:
            return []
        
        # Preprocess query
        processed_query = self.preprocess_text(query)
        
        # Transform query using the same vectorizer
        query_vector = self.tfidf_vectorizer.transform([processed_query])
        
        # Calculate cosine similarity
        similarity_scores = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
        
        # Get top results
        top_indices = similarity_scores.argsort()[-max_results * 2:][::-1]
        
        # Filter out results with very low similarity
        results = []
        for idx in top_indices:
            if similarity_scores[idx] > 0.01:  # Minimum similarity threshold
                results.append({
                    'url': self.document_urls[idx],
                    'title': self.document_titles[idx],
                    'content_snippet': self.get_snippet(self.documents[idx], query),
                    'similarity_score': similarity_scores[idx],
                    'page_rank': self.calculate_page_rank([self.document_urls[idx]])[0]
                })
        
        # Combine similarity and page rank for final scoring
        for result in results:
            result['final_score'] = result['similarity_score'] * result['page_rank']
        
        # Sort by final score
        results.sort(key=lambda x: x['final_score'], reverse=True)
        
        return results[:max_results]
    
    def get_snippet(self, content, query, max_length=200):
        """Extract relevant snippet from content"""
        query_words = query.lower().split()
        content_lower = content.lower()
        
        # Find the best position to start the snippet
        best_pos = 0
        best_score = 0
        
        for i in range(0, len(content) - max_length, 50):
            snippet = content_lower[i:i + max_length]
            score = sum(1 for word in query_words if word in snippet)
            if score > best_score:
                best_score = score
                best_pos = i
        
        snippet = content[best_pos:best_pos + max_length]
        
        # Highlight query terms (basic implementation)
        for word in query_words:
            pattern = re.compile(re.escape(word), re.IGNORECASE)
            snippet = pattern.sub(f'**{word}**', snippet)
        
        return snippet.strip() + ('...' if len(content) > best_pos + max_length else '')
    
    def suggest_spelling(self, query):
        """Basic spelling suggestion based on document terms"""
        if not hasattr(self.tfidf_vectorizer, 'vocabulary_'):
            return []
        
        vocabulary = list(self.tfidf_vectorizer.vocabulary_.keys())
        query_words = query.lower().split()
        suggestions = []
        
        for word in query_words:
            if word not in vocabulary:
                # Find similar words using edit distance
                similar_words = []
                for vocab_word in vocabulary:
                    if abs(len(word) - len(vocab_word)) <= 2:
                        # Simple edit distance check
                        if self.edit_distance(word, vocab_word) <= 2:
                            similar_words.append(vocab_word)
                
                if similar_words:
                    suggestions.extend(similar_words[:3])
        
        return suggestions
    
    def edit_distance(self, s1, s2):
        """Calculate edit distance between two strings"""
        if len(s1) < len(s2):
            return self.edit_distance(s2, s1)
        
        if len(s2) == 0:
            return len(s1)
        
        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        
        return previous_row[-1]

if __name__ == "__main__":
    # Test the search engine
    engine = SearchEngine()
    
    # Example searches
    test_queries = ["python programming", "web development", "machine learning"]
    
    for query in test_queries:
        print(f"\nSearching for: '{query}'")
        results = engine.search(query, max_results=5)
        
        for i, result in enumerate(results, 1):
            print(f"{i}. {result['title']}")
            print(f"   URL: {result['url']}")
            print(f"   Score: {result['final_score']:.4f}")
            print(f"   Snippet: {result['content_snippet'][:100]}...")
            print()
