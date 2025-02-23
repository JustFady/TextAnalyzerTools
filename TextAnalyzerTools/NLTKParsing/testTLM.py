# The function returns None for an empty treebank tag.
from TLM import calculate_similarity_score
from TLM import get_wordnet_pos



def test_none_for_empty_tag(self):
    assert get_wordnet_pos('') == None
    assert get_wordnet_pos(None) == None


    # Function prompts user for input sentences
def test_prompt_user_input(self):
    result = get_input_sentences()
    
    assert isinstance(result, tuple)
    assert len(result) == 2
    assert isinstance(result[0], str)
    assert isinstance(result[1], str)
    
    # The function should return a similarity score of 1.0 when the same sentence is passed as both arguments.
def test_same_sentence_similarity_score(self):
    sentence = "This is a test sentence."
    similarity_score = calculate_similarity_score(sentence, sentence)
    assert similarity_score == 1.0
        
# The function should return the correct similarity score between two sentences.
def test_calculate_similarity_score(self):
    sentence1 = "The cat is on the mat"
    sentence2 = "The dog is on the mat"
    assert calculate_similarity_score(sentence1, sentence2) == 0.5

    sentence1 = "The cat is on the mat"
    sentence2 = "The cat is on the mat"
    assert calculate_similarity_score(sentence1, sentence2) == 1.0

    sentence1 = "The cat is on the mat"
    sentence2 = "The cat is not on the mat"
    assert calculate_similarity_score(sentence1, sentence2) == 0.75