from flask import Flask, render_template, request
from transformers import BartForConditionalGeneration, BartTokenizer
import torch

app = Flask(__name__)

# Load model and tokenizer once (expensive to reload each time)
tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")
model = BartForConditionalGeneration.from_pretrained("facebook/bart-large-cnn")

def summarize_with_bart(text, max_length=80, min_length=10):
    inputs = tokenizer([text], max_length=1024, return_tensors="pt", truncation=True)
    summary_ids = model.generate(
        inputs["input_ids"],
        num_beams=4,
        min_length=min_length,
        max_length=max_length,
        early_stopping=True
    )
    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)

@app.route("/", methods=["GET", "POST"])
def index():
    summary = ""
    if request.method == "POST":
        text = request.form["text"]
        if text.strip():
            summary = summarize_with_bart(text)
    return render_template("index.html", summary=summary)

# from flask import Flask, render_template, request, jsonify

# @app.route("/", methods=["POST"])
# def summarize_api():
#     text = request.form.get("text", "")
#     if text.strip():
#         summary = summarize_with_bart(text)
#         return jsonify({"summary": summary})
#     return jsonify({"summary": ""})


if __name__ == "__main__":
    app.run(debug=True)