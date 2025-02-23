import nltk
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.corpus import treebank


# Download NLTK resources if not already downloaded
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('treebank')

# Sample sentence
sentence = "What should I do with my time?"

# Tokenize the sentence into words
words = word_tokenize(sentence)

# Tag each word with its part of speech
pos_tags = pos_tag(words)

# Display the tagged words with their POS
print(pos_tags)

# Load a sample parse tree from the treebank corpus and draw it
t = treebank.parsed_sents('wsj_0001.mrg')[0]
t.draw()

#SET TK_SILENCE_DEPRECIATION N=1

#whats the better version of this python language interperter, 
#https://stackoverflow.com/questions/74972873/tkinter-deprecation-warning
#https://www.nltk.org/_modules/nltk/tag/perceptron.html