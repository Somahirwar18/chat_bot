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
from chatbot import chat

app = Flask(__name__)

with open("config.json") as file:
    data = json.load(file)

WEBHOOK_VERIFY_TOKEN = data['WEBHOOK_VERIFY_TOKEN']
GRAPH_API_TOKEN = data['GRAPH_API_TOKEN']

# send the response as a WhatsApp message back to the user
def send_whatsapp_message(body, message):
    value = body["entry"][0]["changes"][0]["value"]
    phone_number_id = value["metadata"]["phone_number_id"]
    from_number = value["messages"][0]["from"]
    headers = {
        "Authorization": f"Bearer {GRAPH_API_TOKEN}",
        "Content-Type": "application/json",
    }
    url = "https://graph.facebook.com/v20.0/" + phone_number_id + "/messages"
    data = {
        "messaging_product": "whatsapp",
        "to": from_number,
        "type": "text",
        "text": {"body": message},
    }
    response = requests.post(url, json=data, headers=headers)
    print(f"whatsapp message response: {response.json()}")
    response.raise_for_status()

# handle WhatsApp messages of different type
def handle_whatsapp_message(body):
    message = body["entry"][0]["changes"][0]["value"]["messages"][0]
    # if message["type"] == "text":
    message_body = message["text"]["body"]
    # elif message["type"] == "audio":
    #     audio_id = message["audio"]["id"]
    #     message_body = handle_audio_message(audio_id)
    # response = make_openai_request(message_body, message["from"])
    response = chat(message_body)
    send_whatsapp_message(body, response)

# handle incoming webhook messages
def handle_message(request):
    # Parse Request body in json format
    body = request.get_json()
    print(f"request body: {body}")

    try:
        # info on WhatsApp text message payload:
        # https://developers.facebook.com/docs/whatsapp/cloud-api/webhooks/payload-examples#text-messages
        if body.get("object"):
            if (
                body.get("entry")
                and body["entry"][0].get("changes")
                and body["entry"][0]["changes"][0].get("value")
                and body["entry"][0]["changes"][0]["value"].get("messages")
                and body["entry"][0]["changes"][0]["value"]["messages"][0]
            ):
                handle_whatsapp_message(body)
            return jsonify({"status": "ok"}), 200
        else:
            # if the request is not a WhatsApp API event, return an error
            return (
                jsonify({"status": "error", "message": "Not a WhatsApp API event"}),
                404,
            )
    # catch all other errors and return an internal server error
    except Exception as e:
        print(f"unknown error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


def verify(request):
    # Parse params from the webhook verification request
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    # Check if a token and mode were sent
    if mode and token:
        # Check the mode and token sent are correct
        if mode == "subscribe" and token == WEBHOOK_VERIFY_TOKEN:
            # Respond with 200 OK and challenge token from the request
            print("WEBHOOK_VERIFIED")
            return challenge, 200
        else:
            # Responds with '403 Forbidden' if verify tokens do not match
            print("VERIFICATION_FAILED")
            return jsonify({"status": "error", "message": "Verification failed"}), 403
    else:
        # Responds with '400 Bad Request' if verify tokens do not match
        print("MISSING_PARAMETER")
        return jsonify({"status": "error", "message": "Missing parameters"}), 400


@app.route("/", methods=["GET"])
def home():
    return "WhatsApp OpenAI Webhook is listening!"


# Accepts POST and GET requests at /webhook endpoint
@app.route("/webhook", methods=["POST", "GET"])
def webhook():
    if request.method == "GET":
        return verify(request)
    elif request.method == "POST":
        return handle_message(request)