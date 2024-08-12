# from flask import Flask, request, jsonify
# from chatbot import chat
# import json
# import requests


# app = Flask(__name__)


# with open("config.json") as file:
#     data = json.load(file)

# WEBHOOK_VERIFY_TOKEN = data['WEBHOOK_VERIFY_TOKEN']
# GRAPH_API_TOKEN = data['GRAPH_API_TOKEN']

# print("WEBHOOK_VERIFY_TOKEN - " , WEBHOOK_VERIFY_TOKEN)
# print("GRAPH_API_TOKEN - " , GRAPH_API_TOKEN)

# @app.route('/webhook', methods=['POST'])
# def echo():
#     data = request.get_json()
#     # message = data['message']
#     msg = data.body.entry[0].changes[0].value.messages[0]
#     if (msg.type == "text"):
#         business_phone_number_id = data.body.entry[0].changes[0].value.metadata.phone_number_id
#         url = f"https://graph.facebook.com/v18.0/{business_phone_number_id}/messages"
#         headers = {
#             "Authorization": f"Bearer {GRAPH_API_TOKEN}",
#             "Content-Type": "application/json"  # Optional, but ensures the correct content type
#         }
#         data = {
#             "messaging_product": "whatsapp",
#             "to": msg["from"],
#             "text": {"body": "Echo: " + msg["text"]["body"]},
#             "context": {
#                 "message_id": msg["id"]  # shows the message as a reply to the original user message
#             }
#         }
#         response = requests.post(url, headers=headers, json=data)
#         # return response.json()  # Optional: return the response from the API

#     # print(data)
#     if not data:
#         return jsonify({"error": "No data provided"}), 400

#     return jsonify({"received_data": chat(message)}), 200

# if __name__ == '__main__':
#     app.run(host="0.0.0.0", port=5000)

import os
import json
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load environment variables
WEBHOOK_VERIFY_TOKEN = os.getenv('WEBHOOK_VERIFY_TOKEN')
GRAPH_API_TOKEN = os.getenv('GRAPH_API_TOKEN')
PORT = int(os.getenv('PORT', 5000))  # Default to port 5000 if not set

@app.route('/webhook', methods=['POST'])
def webhook():
    # Log incoming messages
    print("Incoming webhook message:", json.dumps(request.json, indent=2))

    # Check if the webhook request contains a message
    message = request.json.get('entry', [])[0].get('changes', [])[0].get('value', {}).get('messages', [])[0]

    # Check if the incoming message contains text
    if message and message.get('type') == 'text':
        # Extract the business number to send the reply from it
        business_phone_number_id = request.json.get('entry', [])[0].get('changes', [])[0].get('value', {}).get('metadata', {}).get('phone_number_id')

        # Send a reply message as per the docs
        reply_url = f"https://graph.facebook.com/v18.0/{business_phone_number_id}/messages"
        headers = {
            "Authorization": f"Bearer {GRAPH_API_TOKEN}",
            "Content-Type": "application/json"
        }
        data = {
            "messaging_product": "whatsapp",
            "to": message['from'],
            "text": {"body": "Echo: " + message['text']['body']},
            "context": {
                "message_id": message['id']  # shows the message as a reply to the original user message
            }
        }
        response = requests.post(reply_url, headers=headers, json=data)
        print("Message sent:", response.status_code)

        # Mark incoming message as read
        read_data = {
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id": message['id']
        }
        response = requests.post(reply_url, headers=headers, json=read_data)
        print("Message marked as read:", response.status_code)

    return jsonify({'status': 'success'}), 200

@app.route('/webhook', methods=['GET'])
def verify_webhook():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    # Check the mode and token sent are correct
    if mode == "subscribe" and token == WEBHOOK_VERIFY_TOKEN:
        # Respond with 200 OK and challenge token from the request
        print("Webhook verified successfully!")
        return challenge, 200
    else:
        # Respond with '403 Forbidden' if verify tokens do not match
        return 'Forbidden', 403

@app.route('/')
def home():
    return "<pre>Nothing to see here.\nCheckout README.md to start.</pre>", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
