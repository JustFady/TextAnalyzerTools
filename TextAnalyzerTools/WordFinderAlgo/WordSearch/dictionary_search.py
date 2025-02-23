import json
import os
import time
import pandas as pd
import boto3

s3 = boto3.client('s3')
bucket_name = 'parsimony-words'  # Update as needed
DATA_DIR = '/Users/fadyyoussef/Downloads/s3Objects'

# Use paginator to list all objects in the S3 bucket
paginator = s3.get_paginator('list_objects_v2')
pages = paginator.paginate(Bucket=bucket_name)


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
    except Exception:
        print(f"File {file_name} not found in S3 or an error occurred.")
        return None

        
        # Load JSON file (local first, then S3)
def load_file(file_name):
    data = load_local_json(file_name)
    if data is not None:
        return data
    else:
        print(f"{file_name} not found locally. Attempting to download from S3.")
        data = load_s3_json(file_name)
        if data is not None:
            return data
        else:
            print(f"{file_name} not found in S3.")
            return None

# Get the definition based on the full word tag (e.g., 'apple_n', 'book_n')
def get_definition_local(word_tag, data):
    if word_tag in data:
        return data[word_tag].get('definition', f"Definition for '{word_tag}' not found.")
    return f"Definition for '{word_tag}' not found."

def get_definition_s3(word_tag, data):
    definitions = data.get("definitions", {})
    if word_tag in definitions:
        return definitions[word_tag]
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
    
    ## what is PRO in pos? 'a_PRO.json
    ## what is PTCL in pos? 'a_PTCL.json

# Get the definitions for each word in the sentence
def get_sentence_definitions(sentence):
    word_definitions = {}
    words = sentence.split()

    for word_tag in words:
        word_type, base_word = get_word_and_type(word_tag)
        file_name = f"{base_word}.json"  # Expecting files like 'apple.json'
        data = load_file(file_name)
        
        if data:
            definition = get_definition_s3(word_tag, data)
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

#change to fit new json files

# Run a test case and return the results in a DataFrame
def run_test_case(word_list):
    results = []
    for word_tag in word_list:
        word_type, base_word = get_word_and_type(word_tag)
        file_name = f"{base_word}.json"
        data = load_file(file_name)
        
        if data:
            definition = get_definition_s3(word_tag, data)
            results.append([word_tag, word_type, definition])
        else:
            results.append([word_tag, word_type, f"Definition for '{word_tag}' not found."])

    return pd.DataFrame(results, columns=['Word', 'Part of Speech', 'Definition'])

# Measure the time it takes to run a test case and store the result in a DataFrame
def run_tests_with_time(test_cases):
    for word_list in test_cases:
        start_time = time.time()
        df = run_test_case(word_list)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"\nTest case with {len(word_list)} words:")
        print(df)
        print(f"Execution time: {elapsed_time:.4f} seconds")

# Allow user to input a sentence and get definitions with runtime
def run_custom_input():
    sentence = input("Enter objects ( _N, _V): ")
    if sentence.strip():
        start_time = time.time()
        df = run_test_case(sentence.split())
        end_time = time.time()
        elapsed_time = end_time - start_time
        print("\nDefinitions in dictionary format:")
        print(df)
        print(f"Execution time: {elapsed_time:.4f} seconds")

# Allow user to select predefined tests (5, 10, 25, 50, or 100 words)
def run_predefined_test():
    test_cases = {
        1: ["apple_n", "book_n", "bottle_n", "car_n", "cat_n"],
        2: ["apple_n", "book_n", "bottle_n", "car_n", "cat_n", "chair_n", "dog_n", "laptop_n", "phone_n", "watch_n"],
        3: ["apple_n", "book_n", "bottle_n", "car_n", "cat_n", "chair_n", "dog_n", "laptop_n", "phone_n", "watch_n",
            "apple_v", "book_v", "bottle_v", "car_v", "cat_v", "chair_v", "dog_v", "laptop_v", "phone_v", "watch_v",
            "apple_adj", "book_adj", "bottle_adj", "car_adj", "cat_adj"],
        4: (["apple_n", "book_n", "bottle_n", "car_n", "cat_n", "chair_n", "dog_n", "laptop_n", "phone_n", "watch_n",
            "apple_v", "book_v", "bottle_v", "car_v", "cat_v", "chair_v", "dog_v", "laptop_v", "phone_v", "watch_v",
            "apple_adj", "book_adj", "bottle_adj", "car_adj", "cat_adj"] * 2),
        5: (["apple_n", "book_n", "bottle_n", "car_n", "cat_n", "chair_n", "dog_n", "laptop_n", "phone_n", "watch_n",
            "apple_v", "book_v", "bottle_v", "car_v", "cat_v", "chair_v", "dog_v", "laptop_v", "phone_v", "watch_v",
            "apple_adj", "book_adj", "bottle_adj", "car_adj", "cat_adj"] * 4)
    }
    print("Select a test case:")
    for key, words in test_cases.items():
        print(f"{key}. {len(words)} words")

    choice = int(input("Enter your choice: "))
    word_list = test_cases.get(choice)
    
    if word_list:
        run_tests_with_time([word_list])
    else:
        print("Invalid choice. Try again.")

if __name__ == "__main__":
    while True:
        print("\nChoose an option:")
        print("1. Input a sentence and get definitions with runtime.")
        print("2. Run a predefined test (5, 10, 25, 50, or 100 words).")
        print("3. Exit.")
        choice = int(input("Enter your choice: "))
        
        if choice == 1:
            run_custom_input()
        elif choice == 2:
            run_predefined_test()
        elif choice == 3:
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")