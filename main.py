import os
import re
import json
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize Gemini API client explicitly for Hugging Face Secrets
try:
    api_key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
except Exception as e:
    client = None
    print(f"Failed to initialize GenAI client: {e}")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze_code():
    if not client:
        return jsonify({"error": "API client not initialized. Check your GEMINI_API_KEY.", "fixed_code": ""}), 500
        
    data = request.json
    if not data or "code" not in data:
        return jsonify({"error": "No code provided", "fixed_code": ""}), 400
        
    user_code = data.get("code")
    language = data.get("language", "python")
    
    prompt = f"""Act as an expert software engineer. Analyze the following code:
```{language}
{user_code}
```

Identify the specific error.
Explain it in 2 sentences.
Provide the full corrected code block.

Return ONLY a valid JSON object with the following structure (no markdown styling around the JSON like ```json):
{{
  "explanation": "...",
  "fixed_code": "..."
}}
"""
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        
        response_text = response.text.strip()
        
        # Strip potential markdown formatting if the model still includes it
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
            
        result = json.loads(response_text)
        
        return jsonify({
            "error": result.get("explanation", "Could not parse explanation."),
            "fixed_code": result.get("fixed_code", "")
        })
        
    except json.JSONDecodeError:
        return jsonify({"error": "The bug is too powerful, try again! AI returned invalid data.", "fixed_code": response_text}), 500
    except Exception as e:
        print(f"Error during AI analysis: {e}")
        return jsonify({"error": f"Analysis failed: {str(e)}", "fixed_code": ""}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    app.run(host="0.0.0.0", port=port, debug=True)
