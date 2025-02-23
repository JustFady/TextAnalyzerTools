import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from nltk import pos_tag

# Download NLTK resources if not already downloaded
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('stopwords')

# Function to preprocess a sentence
def preprocess_sentence(sentence):
    # Tokenize the sentence into words
    words = word_tokenize(sentence)
    
    # Remove stopwords, punctuation, and convert to lowercase
    filtered_words = [word.lower() for word in words 
                      if word.isalnum() and word.lower() not in stopwords.words('english')]
    
    # Tag the words with their part of speech
    pos_tags = pos_tag(filtered_words)
    
    # Lemmatize the words and map them to their corresponding synsets
    synsets = []
    for word, tag in pos_tags:
        # Determine the part of speech for WordNet lemmatization
        wordnet_pos = get_wordnet_pos(tag)
        # Get the synsets of the word based on its part of speech
        synset = wn.synsets(word, pos=wordnet_pos)
        if synset:
            # Store both the word and its synset
            synsets.append((word, synset[0]))
    return synsets

# Function to get the part of speech of a word
def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wn.ADJ
    elif treebank_tag.startswith('V'):
        return wn.VERB
    elif treebank_tag.startswith('N'):
        return wn.NOUN
    elif treebank_tag.startswith('R'):
        return wn.ADV
    else:
        return None

# Function to calculate the similarity score between two sentences
def calculate_similarity_score(sentence1, sentence2):
    synsets1 = preprocess_sentence(sentence1)
    synsets2 = preprocess_sentence(sentence2)
    
    similarity_scores = []
    for _, synset1 in synsets1:
        for _, synset2 in synsets2:
            # Calculate the path similarity between synsets of words
            similarity = wn.path_similarity(synset1, synset2)
            if similarity:
                similarity_scores.append(similarity)
    
    if similarity_scores:
        # Calculate the average similarity score
        average_similarity_score = sum(similarity_scores) / len(similarity_scores)
        return average_similarity_score
    else:
        return 0

# Get input sentences from the user
sentence1 = input("Enter the first sentence: ")
sentence2 = input("Enter the second sentence: ")

# Calculate similarity score between the two sentences
similarity_score = calculate_similarity_score(sentence1, sentence2)
print(f'The similarity score between the two sentences is {similarity_score:.2f}')

# Output the nodes of the inputted sentences
print("\nNodes of Sentence 1:")
for word, synset in preprocess_sentence(sentence1):
    print(f"{word}\n\t Synset: {synset.name().split('.')[0]} 
                   \n\t Definition: {synset.definition()}")

print("\nNodes of Sentence 2:")
for word, synset in preprocess_sentence(sentence2):
    print(f"{word}\n\t Synset: {synset.name().split('.')[0]}
                    \n\t Definition: {synset.definition()}")

    # The function returns None for an empty treebank tag.
    def test_none_for_empty_tag(self):
        assert get_wordnet_pos('') == None
        assert get_wordnet_pos(None) == None


            # The function should return the correct similarity score between two sentences.
    #def test_calculate_similarity_score(self):
      #sentence1 = "The cat is on the mat"
      #sentence2 = "The dog is on the mat"
      #assert calculate_similarity_score(sentence1, sentence2) == 0.5

        #sentence1 = "The cat is on the mat"
        #sentence2 = "The cat is on the mat"
        #assert calculate_similarity_score(sentence1, sentence2) == 1.0

        #sentence1 = "The cat is on the mat"
        #sentence2 = "The cat is not on the mat"
        #assert calculate_similarity_score(sentence1, sentence2) == 0.75