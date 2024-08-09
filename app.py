import tempfile

import streamlit as st

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

from utils import extract_text

MODEL_DIR = "bert-base-parspec"
TOKENIZER = "bert-base-uncased"
CLASSES = ["cable", "fuses", "lighting", "others"]


# Load BERT model and tokenizer
@st.cache_resource
def load_model():
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_DIR)
    tokenizer = AutoTokenizer.from_pretrained(TOKENIZER)
    return model, tokenizer


# Function to classify text using BERT
def classify_text(text, model, tokenizer):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)

    probs = torch.softmax(outputs.logits, dim=-1)
    predictions = torch.argmax(outputs.logits, dim=-1)
    return CLASSES[predictions.item()], probs[0][predictions.item()]


# Streamlit app
def main():
    st.title("PDF Text Extractor and Classifier")

    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

    if uploaded_file is not None:

        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_file:
            temp_file.write(uploaded_file.getbuffer())
            temp_file_path = temp_file.name

            text, first_page_text = extract_text(temp_file_path)
        if text:
            st.text_area("Extracted Text", text, height=300)
            model, tokenizer = load_model()

            if st.button("Predict"):
                class_label, prob = classify_text(first_page_text, model, tokenizer)
                st.write(f"Class Label: {class_label}")
                st.write(f"Probability: {prob: .4f}")
        else:
            st.error("Failed to extract text from the PDF.")


if __name__ == "__main__":
    main()
