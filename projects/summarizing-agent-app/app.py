from flask import Flask, render_template, request
import PyPDF2
from transformers import BartForConditionalGeneration, BartTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

app = Flask(__name__)

# Load BART once
tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")
model = BartForConditionalGeneration.from_pretrained("facebook/bart-large-cnn")

def extract_pdf_text(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def extract_topics(text, num_topics=5):
    # Simple TF-IDF based key phrases
    vectorizer = TfidfVectorizer(stop_words='english', max_features=1000, ngram_range=(1,3))
    X = vectorizer.fit_transform([text])
    feature_array = np.array(vectorizer.get_feature_names_out())
    tfidf_sorting = np.argsort(X.toarray()).flatten()[::-1]
    top_n = feature_array[tfidf_sorting][:num_topics]
    return list(top_n)

def summarize(text, max_length=80, min_length=10):
    inputs = tokenizer([text], max_length=1024, return_tensors="pt", truncation=True)
    summary_ids = model.generate(
        inputs["input_ids"],
        num_beams=4,
        min_length=min_length,
        max_length=max_length,
        early_stopping=True
    )
    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)

def summarize_by_topics(text):
    topics = extract_topics(text)
    short_summaries = {}
    detailed_summaries = {}

    for topic in topics:
        # Extract sentences containing the topic
        sentences = [s for s in text.split('.') if topic.lower() in s.lower()]
        if not sentences:
            sentences = text.split('.')[:3]  # fallback
        topic_text = '. '.join(sentences)

        short_summaries[topic] = summarize(topic_text, max_length=40)
        detailed_summaries[topic] = summarize(topic_text, max_length=100)

    # Final summary: summarize all detailed summaries
    combined_text = ' '.join(detailed_summaries.values())
    final_summary = summarize(combined_text, max_length=120)
    return topics, short_summaries, detailed_summaries, final_summary

@app.route("/", methods=["GET", "POST"])
def index():
    topics, short_summaries, detailed_summaries, final_summary = [], {}, {}, ""
    if request.method == "POST":
        pdf_file = request.files.get("pdf_file")
        if pdf_file:
            text = extract_pdf_text(pdf_file)
            topics, short_summaries, detailed_summaries, final_summary = summarize_by_topics(text)
    return render_template("index.html", 
                           topics=topics, 
                           short_summaries=short_summaries, 
                           detailed_summaries=detailed_summaries, 
                           final_summary=final_summary)

if __name__ == "__main__":
    app.run(debug=True)