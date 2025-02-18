from flask import Flask, request, jsonify
import speech_recognition as sr
import openai
openai migrate

# Set your OpenAI API key here
openai.api_key = "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"

app = Flask(__name__)

@app.route("/speech-to-text", methods=["POST"])
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        # Convert speech to text using Google Speech Recognition API
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")

        # Send the transcribed text to OpenAI and get a response
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",  # You can change this to "gpt-3.5-turbo" if needed
            messages=[
                {"role": "user", "content": text}  # Sending the recognized text as the user message
            ]
        )

        # Extract the response from OpenAI
        chatgpt_answer = response['choices'][0]['message']['content'].strip()

        # Return the OpenAI response as JSON
        return jsonify({"text": text, "chatgpt_response": chatgpt_answer})

    except sr.UnknownValueError:
        return jsonify({"error": "Could not understand the audio."})
    except sr.RequestError:
        return jsonify({"error": "Speech recognition service error."})
    except openai.error.OpenAIError as e:
        return jsonify({"error": f"OpenAI API error: {e}"})
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {e}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
