from flask import Flask, request, render_template
import google.generativeai as genai
import logging
import os
import traceback
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# Setup Flask and logging
app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Load Gemini API key
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Use a model that is guaranteed to work
model = genai.GenerativeModel("models/gemini-1.5-flash")

@app.route("/", methods=["GET", "POST"])
def generate_description():
    description = None
    input_text = request.form.get("input_text")

    try:
        if input_text:
            prompt = (
                f"Write a 2-line inspirational quote and 10 Instagram hashtags based on:\n"
                f"{input_text}\n"
                f"Total output must be under 100 characters."
            )

            response = model.generate_content(prompt)

            if hasattr(response, 'text'):
                description = response.text.strip()
            else:
                description = "Unexpected format from Gemini."

    except Exception as e:
        logging.error(f"Error generating description: {e}")
        traceback.print_exc()
        description = "Error generating description."

    return render_template("index.html", input_text=input_text, description=description)

if __name__ == "__main__":
    app.run(debug=True)
