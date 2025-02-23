import time
import boto3

#client setup
s3 = boto3.client('s3')
bucket = 'parsimony-words' #s3 bucket used
DATA_DIR = '/Users/fadyyoussef/Documents/s3WordFinder/localObjects' #local objects that can be used

def download_files(input_words):
    paginator = s3.get_paginator('list_objects_v2')
    all_pages = paginator.paginate(Bucket=bucket)

    # Convert the input_words list into a set for O(1) lookup
    input_set = set(input_words)
    found_files = set()  # Track downloaded files to avoid duplicates
    
    start = time.time()
    for page in all_pages:#page with word
        for obj in page['Contents']: #word in page
            key = obj['Key'] #key is word
            
            # download if the key is in the input set and not already downloaded
            if key in input_set and key not in found_files:
                print(f"Downloading {key}")
                s3.download_file(bucket, key, f"{DATA_DIR}/{key}")
                found_files.add(key)  #file as downloaded and counted
                
                # Stop if all requested files are downloaded
                if len(found_files) == len(input_set):
                    end = time.time()
                    print(f"Downloaded {len(input_set)} files in {end - start:.2f} seconds.")
                    return
            
def custom_prompt():
    input_words = input("Enter filenames separated by spaces: ").split()
    download_files(input_words)

def run_test(words_list):
    print(f"Running {len(words_list)} word test:")              
    download_files(words_list)

def test_menu():
    t5w = ["abience_N.json", "abstract_N.json", "accidentally_ADV.json", "active_ADJ.json", "adapt_V.json"] #test 5 words 
    t20w = t5w + ["balance_N.json", "barrier_N.json", "basic_ADJ.json", "battery_PN.json", "beginning_N.json",
                     "behavior_N.json", "belief_N.json", "benefit_N.json", "biology_N.json", "biomechanics_N.json",
                     "calculate_V.json", "capacity_N.json", "capitalism_N.json", "carbon_N.json", "cause_V.json"]
    t40w = t20w + ["'aircut_N.json",".com_N.json",".22_N.json","0_N.json","+1_N.json","abaecin_N.json","abagun_N.json",
                   "abaetetuba_PN.json","abaga_PN.json","abadan_PN.json","abienda_PN.json","abiezer_PN.json","abigail_PN.json",
                   "abstringe_V.json","abstrude_V.json","absume_V.json","absurdify_V.json","abuse_V.json","accinge_V.json", "accite_V.json"]
    
    while True:#options
        print("\nChoose a test:")
        print("1. Test with 5 words")
        print("2. Test with 20 words")
        print("3. Test with 40 words")
        print("4. Go back to the main menu")
        
        choice = input("Enter your choice: ")
        if choice == '1':
            run_test(t5w)
        elif choice == '2':
            run_test(t20w)
        elif choice == '3':
            run_test(t40w)
        elif choice == '4':
            print("Returning...")
            break
        else:
            print("Invalid input, please try again...")

def main():
    while True:
        print("\nChoose an option:")
        print("1. Custom prompt input to download specific files.")
        print("2. Run a test with predefined word counts.")
        print("3. Exit.")
        
        choice = input("Enter your choice: ")
        if choice == '1':
            custom_prompt()    
        elif choice == '2':
            test_menu()
        elif choice == '3':
            print("\nExiting...")
            break
        else:
            print("Invalid input, please try again...")

if __name__ == "__main__":
    main()
