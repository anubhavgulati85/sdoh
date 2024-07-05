# app/nlp_model.py

import spacy

nlp = spacy.load('en_core_web_sm')

def extract_sdoh_keywords(text):
    doc = nlp(text)
    sdoh_keywords = [token.text for token in doc if token.text.lower() in ['housing', 'income', 'education', 'employment', 'nutrition', 'transportation']]
    return sdoh_keywords
