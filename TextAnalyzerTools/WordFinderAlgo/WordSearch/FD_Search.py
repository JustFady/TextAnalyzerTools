import json
import os
import time
import pandas as pd

# Directory where your JSON files are stored
DATA_DIR = '/Users/fadyyoussef/Downloads/s3Objects'

# Load the JSON file from the directory
def load_file(file_name):
    full_path = os.path.join(DATA_DIR, file_name)
    try:
        with open(full_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File {file_name} not found.")
        return None

# Get the definition based on the full word tag (e.g., 'apple_n', 'book_n')
def get_definition(word_tag, data):
    if word_tag in data:
        return data[word_tag].get('definition', f"Definition for '{word_tag}' not found.")
    return f"Definition for '{word_tag}' not found."

# Determine the word type based on the suffix (e.g., '_n' for noun)
def get_word_and_type(word_tag):
    if word_tag.endswith('_n'):
        return 'noun', word_tag.split('_')[0]
    elif word_tag.endswith('_v'):
        return 'verb', word_tag.split('_')[0]
    elif word_tag.endswith('_adj'):
        return 'adjective', word_tag.split('_')[0]
    elif word_tag.endswith('_adv'):
        return 'adverb', word_tag.split('_')[0]
    elif word_tag.endswith('_conj'):
        return 'conjunction', word_tag.split('_')[0]
    elif word_tag.endswith('_prep'):
        return 'preposition', word_tag.split('_')[0]
    else:
        return 'unknown', word_tag.split('_')[0]

# Group words by part of speech into separate lists
def get_sentence_definitions(sentence):
    word_definitions = {
        "nouns": [],
        "verbs": [],
        "adjectives": [],
        "adverbs": [],
        "conjunctions": [],
        "prepositions": [],
        "unknown": []
    }

    words = sentence.split()

    for word_tag in words:
        word_type, base_word = get_word_and_type(word_tag)
        file_name = f"{base_word}.json"  # Expecting file like apple.json
        data = load_file(file_name)
        
        if data:
            definition = get_definition(word_tag, data)  # Use full word tag (e.g., 'apple_n')
        else:
            definition = f"Definition for '{word_tag}' not found."

        # Append to the correct part of speech list
        if word_type in word_definitions:
            word_definitions[word_type].append((word_tag, definition))
        else:
            word_definitions["unknown"].append((word_tag, definition))

    return word_definitions

# Run a test case and return the results grouped by part of speech
def run_test_case(word_list):
    word_definitions = {
        "nouns": [],
        "verbs": [],
        "adjectives": [],
        "adverbs": [],
        "conjunctions": [],
        "prepositions": [],
        "unknown": []
    }

    for word_tag in word_list:
        word_type, base_word = get_word_and_type(word_tag)
        file_name = f"{base_word}.json"
        data = load_file(file_name)
        
        if data:
            definition = get_definition(word_tag, data)  # Use the full word_tag (e.g., 'apple_n')
        else:
            definition = f"Definition for '{word_tag}' not found."

        # Append the word and definition to the appropriate list
        if word_type in word_definitions:
            word_definitions[word_type].append((word_tag, definition))
        else:
            word_definitions["unknown"].append((word_tag, definition))

    # Print results grouped by part of speech
    for pos, words in word_definitions.items():
        if words:
            print(f"\n{pos.capitalize()}:")
            for word_tag, definition in words:
                print(f"  {word_tag}: {definition}")

    return word_definitions

# Measure the time it takes to run a test case and display grouped by part of speech
def run_tests_with_time(test_cases):
    for word_list in test_cases:
        start_time = time.time()
        run_test_case(word_list)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"\nExecution time: {elapsed_time:.4f} seconds")

# Allow user to input a sentence and get definitions grouped by part of speech
def run_custom_input():
    sentence = input("Enter a sentence (e.g., 'apple_n book_n watch_n'): ")
    if sentence.strip():
        try:
            start_time = time.time()
            run_test_case(sentence.split())
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"\nExecution time: {elapsed_time:.4f} seconds")
        except Exception as e:
            print(f"Error processing input: {e}")
            print("Returning to main menu.")
            return

# Allow user to select predefined tests (5, 10, 25, 50, or 100 words)
def run_predefined_test():
    tc_options = {
        1: "5 words",
        2: "10 words",
        3: "25 words",
        4: "50 words",
        5: "100 words"
    }

    # Predefined test cases using only existing JSON objects
    tc_5 = ["apple_n", "book_n", "bottle_n", "car_n", "cat_n"]
    tc_10 = tc_5 + ["chair_n", "dog_n", "laptop_n", "phone_n", "watch_n"]
    tc_25 = tc_10 + ["apple_v", "book_v", "bottle_v", "car_v", "cat_v", "chair_v", "dog_v", 
                         "laptop_v", "phone_v", "watch_v", "apple_adj", "book_adj", "bottle_adj", 
                         "car_adj", "cat_adj"]
    tc_50 = tc_25 * 2 
    tc_100 = tc_50 * 2  

    print("Select a test case:")
    for key, value in tc_options.items():
        print(f"{key}. {value}")

    try:
        choice = int(input("Enter your choice: "))
        if choice == 1:
            run_tests_with_time([tc_5])
        elif choice == 2:
            run_tests_with_time([tc_10])
        elif choice == 3:
            run_tests_with_time([tc_25])
        elif choice == 4:
            run_tests_with_time([tc_50])
        elif choice == 5:
            run_tests_with_time([tc_100])
        else:
            print("Invalid choice. Returning to main menu.")
    except ValueError:
        print("Invalid input. Please enter a valid number. Returning to main menu.")

if __name__ == "__main__":
    while True:
        print("\nChoose an option:")
        print("1. Input a sentence and get definitions grouped by part of speech.")
        print("2. Run a predefined test (5, 10, 25, 50, or 100 words).")
        print("3. Exit.")
        try:
            choice = int(input("Enter your choice: "))
            if choice == 1:
                run_custom_input()
            elif choice == 2:
                run_predefined_test()
            elif choice == 3:
                print("Exiting...")
                break
            else:
                print("Invalid choice. Returning to main menu.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")