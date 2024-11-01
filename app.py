from flask import Flask, render_template, request, jsonify
import random
import json

app = Flask(__name__)

# Load responses from JSON file
with open('responses.json') as f:
    responses = json.load(f)

# Initialize a simple memory dictionary for context
context = {"last_intent": None}

def misinterpret(user_input):
    global context  # Access the global context variable
    
    user_input = user_input.lower().split()
    for word in user_input:
        # Check for specific intents
        if word in responses:
            context["last_intent"] = word  # Update context with the current intent
            return random.choice(responses[word])
    
    # Check for follow-up based on last intent (e.g., "another one")
    if "another" in user_input and context["last_intent"]:
        return random.choice(responses.get(context["last_intent"], ["I’m still thinking about that!"]))
    
    # Default response if no match found
    return "I think you're talking about a lost sock!"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['user_input']
    bot_response = misinterpret(user_input)
    return jsonify({'response': bot_response})

if __name__ == "__main__":
    app.run(debug=True)
