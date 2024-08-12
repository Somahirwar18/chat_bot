import nltk
from nltk.chat.util import Chat, reflections

# Download the NLTK data needed for tokenization and other processing
nltk.download('punkt')


# Define pairs of patterns and responses
pairs = [
    [
        r"my name is (.*)",
        ["Hello %1, how can I assist you today?",]
    ],
    [
        r"hi|hey|hello",
        ["Hello!", "Hey there!", "Hi!"]
    ],
    [
        r"what is your name?",
        ["I'm a chatbot created by you. What's your name?",]
    ],
    [
        r"how are you?",
        ["I'm just a bot, but I'm doing great! How about you?",]
    ],
    [
        r"sorry (.*)",
        ["It's okay.", "No problem!",]
    ],
    [
        r"I am (.*) (good|well|okay|great)",
        ["Glad to hear that!", "That's good to know."]
    ],
    [
        r"(.*) (location|city)",
        ["I'm just in the cloud, but where are you from?"]
    ],
    [
        r"quit",
        ["Bye! Take care.", "Goodbye!"]
    ],
    [
        r"(.*)",
        ["I'm sorry, I don't understand that. Can you rephrase?"]
    ],
]

# Reflects words like "I'm" to "you are" for more natural responses
reflections = {
    "i am"       : "you are",
    "i was"      : "you were",
    "i"          : "you",
    "i'm"        : "you are",
    "i'd"        : "you would",
    "i've"       : "you have",
    "i'll"       : "you will",
    "my"         : "your",
    "you are"    : "I am",
    "you were"   : "I was",
    "you've"     : "I have",
    "you'll"     : "I will",
    "your"       : "my",
    "yours"      : "mine",
    "you"        : "me",
    "me"         : "you"
}


# Create a chatbot instance
chatbot = Chat(pairs, reflections)


def chat(user_input):
    # print("Hello! I'm a simple chatbot. Type 'quit' to exit.")
    # while True:
    #     user_input = input("> ")
    #     if user_input.lower() == "quit":
    #         print("Goodbye!")
    #         break
        response = chatbot.respond(user_input)
        return response
