import os
from groq import Groq
from dotenv import load_dotenv
from flask import Flask, request, jsonify

app = Flask(__name__)

# Initialize the Groq client with your API key
api_key = os.getenv("GROQ_API_KEY")
client = Groq(
    api_key=api_key,
)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        # Get the user input from the POST request
        user_input = request.json.get('message')

        if not user_input:
            return jsonify({"error": "No message provided"}), 400

        # Call the Groq API to generate the chat completion
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": user_input,
                }
            ],
            model="llama3-8b-8192",
        )

        # Extract the response from the model
        model_response = chat_completion.choices[0].message.content

        # Return the model's response as JSON
        return jsonify({"response": model_response}), 200

    except Exception as e:
        # Handle any errors and return a generic error message
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
