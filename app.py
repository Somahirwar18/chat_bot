from flask import Flask, request, jsonify
from chatbot import chat
import json
import requests


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
    msg = data.body.entry[0].changes[0].value.messages[0]
    if (msg.type == "text"):
        business_phone_number_id = data.body.entry[0].changes[0].value.metadata.phone_number_id
        url = f"https://graph.facebook.com/v18.0/{business_phone_number_id}/messages"
        headers = {
            "Authorization": f"Bearer {GRAPH_API_TOKEN}",
            "Content-Type": "application/json"  # Optional, but ensures the correct content type
        }
        data = {
            "messaging_product": "whatsapp",
            "to": msg["from"],
            "text": {"body": "Echo: " + msg["text"]["body"]},
            "context": {
                "message_id": msg["id"]  # shows the message as a reply to the original user message
            }
        }
        response = requests.post(url, headers=headers, json=data)
        # return response.json()  # Optional: return the response from the API

    # print(data)
    if not data:
        return jsonify({"error": "No data provided"}), 400

    return jsonify({"received_data": chat(message)}), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
