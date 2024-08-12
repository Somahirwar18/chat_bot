from flask import Flask, request, jsonify
from chatbot import chat
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def echo():
    data = request.get_json()
    message = data['message']
    if not data:
        return jsonify({"error": "No data provided"}), 400

    return jsonify({"received_data": chat(message)}), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
