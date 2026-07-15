from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import requests
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("OPENROUTER_API_KEY")   

print("API KEY:", API_KEY)

MODEL = "openai/gpt-oss-20b:free"    # Model Name


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():

    data = request.get_json()                #Get user's input

    question = data.get("question", "").strip()        

    if question == "":
        return jsonify({
            "answer": "Please enter a question."
        })

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",

        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },

        json={
            "model": MODEL,

            "messages": [
                {
                    "role": "user",
                    "content": question
                }
            ]
        }
    )

    # Print API response in terminal
    print("Status Code:",response.status_code)
    print("Response :",response.text)

    if response.status_code != 200:

        return jsonify({
            "answer": "API Error:\n" + response.text
        })

    result = response.json()

    answer = result["choices"][0]["message"]["content"]

    return jsonify({
        "answer": answer
    })


if __name__ == "__main__":
    app.run(debug=True)