import os
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)
DB_PATH = 'search_engine/database.db'

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    results = []
    if query:
        # Search the database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT url, title FROM pages WHERE content LIKE ?", ('%' + query + '%',))
        results = cursor.fetchall()
        conn.close()
    return jsonify(results)

if __name__ == '__main__':
    if not os.path.exists(os.path.dirname(DB_PATH)):
        os.makedirs(os.path.dirname(DB_PATH))
    app.run(debug=True)

