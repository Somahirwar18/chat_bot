from flask import Flask, request, jsonify
from chatbot import chat
import json


app = Flask(__name__)


with open("config.json") as file:
    data = json.load(file)

WEBHOOK_VERIFY_TOKEN = data['WEBHOOK_VERIFY_TOKEN']
GRAPH_API_TOKEN = data['GRAPH_API_TOKEN']

print("WEBHOOK_VERIFY_TOKEN - " , WEBHOOK_VERIFY_TOKEN)
print("GRAPH_API_TOKEN - " , GRAPH_API_TOKEN)

@app.route('/webhook', methods=['POST'])
def echo():
    data = request.get_json()
    # message = data['message']
    print(data)
    if not data:
        return jsonify({"error": "No data provided"}), 400

    return jsonify({"received_data": chat(message)}), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
