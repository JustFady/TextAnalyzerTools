import json
import os
import time
import pandas as pd
import boto3

# Initialize S3 client
s3 = boto3.client('s3')
bucket_name = 'parsimony-words'  # Update as needed
DATA_DIR = '/Users/fadyyoussef/Documents/s3WordFinder/localObjects'  # Path to local JSON files

# Load JSON from local storage
def load_local_json(file_name):
    path = os.path.join(DATA_DIR, file_name)
    if os.path.exists(path):
        with open(path, 'r') as file:
            return json.load(file)
    else:
        print(f"File {file_name} not found locally.")
        return None

# Download and load JSON from S3
def load_s3_json(file_name):
    try:
        content = s3.get_object(Bucket=bucket_name, Key=file_name)['Body'].read().decode('utf-8')
        return json.loads(content)
    except Exception as e:
        print(f"File {file_name} not found in S3 or an error occurred: {e}")
        return None

# Load JSON file (either from local or S3 based on mode)
def load_file(file_name, mode='local'):
    if mode == 'local':
        return load_local_json(file_name)
    elif mode == 's3':
        return load_s3_json(file_name)
    else:
        print("Invalid mode selected.")
        return None

# Get the definition based on the word tag (e.g., 'apple_n', 'book_n')
def get_definition(word_tag, data):
    if word_tag in data:
        return data[word_tag].get("definition", f"Definition for '{word_tag}' not found.")
    return f"Definition for '{word_tag}' not found."

# Determine the word type based on the suffix (e.g., '_n' for noun)
def get_word_and_type(word_tag):
    tag = word_tag.lower()  # Convert the tag to lowercase for consistent comparison
    if tag.endswith('_n'):
        return 'noun', word_tag.split('_')[0]
    elif tag.endswith('_v'):
        return 'verb', word_tag.split('_')[0]
    elif tag.endswith('_intj'):
        return 'interjection', word_tag.split('_')[0]
    elif tag.endswith('_adj'):
        return 'adjective', word_tag.split('_')[0]
    elif tag.endswith('_adv'):
        return 'adverb', word_tag.split('_')[0]
    elif tag.endswith('_conj'):
        return 'conjunction', word_tag.split('_')[0]
    elif tag.endswith('_prep'):
        return 'preposition', word_tag.split('_')[0]
    elif tag.endswith('_pn'):
        return 'predicate', word_tag.split('_')[0]
    else:
        return 'unknown', word_tag.split('_')[0]

# Get the definitions for each word in the sentence
def get_sentence_definitions(sentence, mode):
    word_definitions = {}
    words = sentence.split()  # Split the sentence into word tags

    for word_tag in words:
        word_type, base_word = get_word_and_type(word_tag)
        file_name = f"{base_word}.json"  # File name based on base word (e.g., 'apple.json')
        data = load_file(file_name, mode=mode)
        
        if data:
            definition = get_definition(word_tag, data)
            word_definitions[word_tag] = {
                "part_of_speech": word_type,
                "definition": definition
            }
        else:
            word_definitions[word_tag] = {
                "part_of_speech": word_type,
                "definition": f"Definition for '{word_tag}' not found."
            }

    return word_definitions

# Run a custom sentence input to get definitions
def run_custom_input(mode):
    sentence = input("Enter a sentence with tagged words (e.g., 'apple_adj book_n'): ")
    start_time = time.time()
    word_definitions = get_sentence_definitions(sentence, mode)
    end_time = time.time()
    elapsed_time = end_time - start_time

    # Display results
    df = pd.DataFrame.from_dict(word_definitions, orient='index')
    print("\nDefinitions in dictionary format:")
    print(df)
    print(f"Execution time: {elapsed_time:.4f} seconds")

# Main function to run the program
if __name__ == "__main__":
    while True:
        print("\nChoose an option:")
        print("1. Input a sentence and get definitions from local files.")
        print("2. Input a sentence and get definitions from S3.")
        print("3. Exit.")
        
        choice = int(input("Enter your choice: "))
        
        if choice == 1:
            run_custom_input(mode='local')
        elif choice == 2:
            run_custom_input(mode='s3')
        elif choice == 3:
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

# got the local search running better
# updated the file strucutre
# still need to search from s3 bucket