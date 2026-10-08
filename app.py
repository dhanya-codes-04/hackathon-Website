from flask import Flask, render_template, request, jsonify
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/simplify", methods=["POST"])
def simplify():

    data = request.get_json()
    policy_text = data.get("text", "")

    if not policy_text.strip():
        return jsonify({
            "error": "Please enter an insurance policy."
        }), 400

    prompt = f"""
You are an Insurance Policy Simplification Assistant.

Your job is to convert complicated insurance policy language
into simple language that an ordinary customer can understand.

IMPORTANT RULES:

1. Do not change the meaning.
2. Do not invent information.
3. Do not remove important conditions.
4. Clearly mention exclusions.
5. Clearly mention important requirements.
6. Explain difficult legal/insurance terms.
7. Use short sentences.
8. Use simple English.
9. If information is missing, say "Not specified in the policy."
10. This is an explanation, not legal or financial advice.

Return the answer in this structure:

SUMMARY:
Give a 2-3 sentence simple summary.

WHAT IS COVERED:
- ...

WHAT IS NOT COVERED:
- ...

IMPORTANT CONDITIONS:
- ...

CLAIM REQUIREMENTS:
- ...

IMPORTANT DATES / LIMITS:
- ...

DIFFICULT TERMS:
- Term: Simple meaning

CUSTOMER FRIENDLY EXPLANATION:
Explain the policy in very simple language.

Here is the insurance policy:

{policy_text}
"""

    try:

        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )

        result = response.text

        return jsonify({
            "result": result
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)