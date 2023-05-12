from flask import Flask, render_template, request
import spacy
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.chat.util import Chat
import re

app = Flask(__name__)

# Initialize spaCy and sentiment analyzer
nlp = spacy.load('en_core_web_sm')
sia = SentimentIntensityAnalyzer()


# Define custom chatbot class
class MyChat(Chat):
    def __init__(self, pairs, reflections={}):
        super().__init__(pairs, reflections)
        self.conversation = []

    def converse(self, message):
        if self.conversation:
            self.conversation.append(("You", message))
        else:
            self.conversation = [("You", message)]

        response = self.respond(message)
        self.conversation.append(("ChatBot", response))
        return response

    def analyze_sentiment(self, message):
        sentiment = sia.polarity_scores(message)
        if sentiment["compound"] >= 0.05:
            return "positive"
        elif sentiment["compound"] <= -0.05:
            return "negative"
        else:
            return "neutral"

    def respond(self, message):
        sentiment = self.analyze_sentiment(message)
        doc = nlp(message)

        # Extract named entities
        entities = []
        for ent in doc.ents:
            entities.append(f"{ent.text} ({ent.label_})")

        # Perform part-of-speech tagging
        pos_tags = [token.pos_ for token in doc]

        # Intent classification
        intent = self.classify_intent(message)

        # Contextual conversation
        context = [msg for _, msg in self.conversation[:-1]]  # Exclude the latest user message

        if intent == "greeting":
            response = self.handle_greeting(context)
        elif intent == "farewell":
            response = self.handle_farewell(context)
        elif intent == "thanks":
            response = self.handle_thanks(context)
        else:
            response = self.handle_unknown(context)

        response += f"\n\nDetected entities: {', '.join(entities)}"
        response += f"\n\nPart-of-speech tags: {', '.join(pos_tags)}"

        return response

    def classify_intent(self, message):
        intents = {
            r"hi|hey|hello": "greeting",
            r"bye|goodbye": "farewell",
            r"thank you|thanks": "thanks"
        }

        for pattern, intent in intents.items():
            if re.search(pattern, message, re.IGNORECASE):
                return intent

        return "unknown"

    def handle_greeting(self, context):
        if any(re.search(r"bye|goodbye", msg, re.IGNORECASE) for msg in context):
            return "Hello again! How can I assist you further?"
        else:
            return "Hello! How can I assist you today?"

    def handle_farewell(self, context):
        return "Goodbye! Take care."

    def handle_thanks(self, context):
        return "You're welcome!"

    def handle_unknown(self, context):
        return "I'm sorry, I didn't understand. Can you please rephrase your message?"


# Define chat pairs
pairs = []

chat = MyChat(pairs)


@app.route("/")
def home():
    if chat.conversation:
        # If conversation history exists, display only bot responses
        conversation = [(role, message) for role, message in chat.conversation if role == "ChatBot"]
    else:
        conversation = []

    return render_template("index.html", conversation=conversation)


@app.route("/get")
def get_bot_response():
    user_msg = request.args.get('msg')
    bot_response = chat.converse(user_msg)
    return bot_response


if __name__ == "__main__":
    app.run(debug=True)


