import os
from groq import Groq
from dotenv import load_dotenv
from flask import Flask, request, jsonify
import speech_recognition as sr
# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Initialize the Groq client with your API key
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY environment variable not set.")

client = Groq(
    api_key=api_key,
)

@app.route("/", methods=['POST'])
def hello():
    return jsonify({"response":"Hello"}), 200


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


@app.route('/stt', methods=['POST'])
def uploadaudio():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = 'audio.wav'
        file.save(filename)
        text = audiototext(filename)
        return jsonify({'text': text})
    
    return jsonify({'error': 'Invalid file format'}), 400

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['wav']


def audiototext(incommingFile):
    r = sr.Recognizer()
    filename = incommingFile

    with sr.AudioFile(filename) as source:
        # listen for the data (load audio to memory)
        audio_data = r.record(source)
        # recognize (convert from speech to text)
        text = r.recognize_google(audio_data)
        print(text)




if __name__ == '__main__':
    # Bind to the port specified by the PORT environment variable
    # port = int(os.environ.get("PORT", 5000))
    # app.run(host='0.0.0.0', port=port)
    app.run(debug=True)
    #audiototext()
