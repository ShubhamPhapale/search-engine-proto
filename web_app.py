from flask import Flask, render_template, request, jsonify
from search_engine import SearchEngine
import os

app = Flask(__name__)
search_engine = None

def initialize_search_engine():
    global search_engine
    db_path = os.path.join(os.path.dirname(__file__), 'database.db')
    search_engine = SearchEngine(db_path)

@app.route('/')
def home():
    return render_template('search.html')

@app.route('/search')
def search():
    query = request.args.get('q', '').strip()
    page = int(request.args.get('page', 1))
    results_per_page = 10
    
    if not query:
        return render_template('search.html', query='', results=[], total_results=0)
    
    # Initialize search engine if not already done
    if search_engine is None:
        initialize_search_engine()
    
    # Perform search
    all_results = search_engine.search(query, max_results=100)
    total_results = len(all_results)
    
    # Pagination
    start_idx = (page - 1) * results_per_page
    end_idx = start_idx + results_per_page
    results = all_results[start_idx:end_idx]
    
    # Calculate pagination info
    total_pages = (total_results + results_per_page - 1) // results_per_page
    has_prev = page > 1
    has_next = page < total_pages
    
    # Get spelling suggestions if no results
    suggestions = []
    if total_results == 0:
        suggestions = search_engine.suggest_spelling(query)
    
    return render_template('search.html', 
                         query=query,
                         results=results,
                         total_results=total_results,
                         page=page,
                         total_pages=total_pages,
                         has_prev=has_prev,
                         has_next=has_next,
                         suggestions=suggestions)

@app.route('/api/search')
def api_search():
    query = request.args.get('q', '').strip()
    max_results = int(request.args.get('max_results', 10))
    
    if not query:
        return jsonify({'error': 'Query parameter is required'}), 400
    
    # Initialize search engine if not already done
    if search_engine is None:
        initialize_search_engine()
    
    results = search_engine.search(query, max_results=max_results)
    
    return jsonify({
        'query': query,
        'total_results': len(results),
        'results': results
    })

@app.route('/api/suggest')
def api_suggest():
    query = request.args.get('q', '').strip()
    
    if not query:
        return jsonify({'suggestions': []})
    
    if search_engine is None:
        initialize_search_engine()
    
    suggestions = search_engine.suggest_spelling(query)
    
    return jsonify({'suggestions': suggestions})

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
    if not os.path.exists(templates_dir):
        os.makedirs(templates_dir)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
