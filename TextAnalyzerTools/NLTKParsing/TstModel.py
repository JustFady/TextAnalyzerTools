import spacy
from spacy import displacy

# Load the language model
nlp = spacy.load("en_core_web_sm")

# Your text here
text = "The quick brown fox jumps over the lazy dog."

# Process the text
doc = nlp(text)

# Generate the dependency parse tree and print it
for token in doc:
    print(f"{token.text:<12}{token.dep_:<10}{token.head.text:<12}{token.head.pos_:<10}{[child for child in token.children]}")

# Visualize the dependency parse tree (optional)
#displacy.serve(doc, style="dep")
