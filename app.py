from flask import Flask, request, jsonify
from rag import get_rag_response

app = Flask(__name__)

@app.route('/')
def home():
    return "RAG Medical API is running!"

@app.route('/query', methods=['POST'])
def query():
    data = request.get_json()
    query = data.get("query")

    if not query:
        return jsonify({"error": "Query not provided"}), 400

    response = get_rag_response(query)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
