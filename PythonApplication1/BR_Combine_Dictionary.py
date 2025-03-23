import json
import os
from BR_Create_Dictionary import write_strongs_dictionary

def merge_dictionaries(dict1, dict2):
    """
    Merges two Strong's dictionaries, appending words from the second dictionary
    to the first dictionary if they are not already present.
    """
    merged_dict = dict1.copy()  # Start with the first dictionary

    for strongs_number, words in dict2.items():
        if strongs_number not in merged_dict:
            # If the Strong's number isn't in the merged dict, add it
            merged_dict[strongs_number] = words
        else:
            # If it exists, append words that are not already present
            existing_words = set(merged_dict[strongs_number])
            for word in words:
                if word not in existing_words:
                    merged_dict[strongs_number].append(word)
                    existing_words.add(word)

    return merged_dict

def load_strongs_dictionary(file_path):
    """
    Loads a Strong's dictionary from a JSON file.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def combine_dictionary_files(DictFile1, DictFile2, DictFileOut):
    """
    Combines two Strong's dictionaries and writes the output to a new file.
    """
    Dict1 = load_strongs_dictionary(DictFile1)  # Load Dictionaries
    Dict2 = load_strongs_dictionary(DictFile2)
    DictOut = merge_dictionaries(Dict1, Dict2)  # Merge Dictionaries
    write_strongs_dictionary(DictOut, DictFileOut)  # Write Dictionary

if __name__ == '__main__':
    BibleRoseDataDir = os.getenv('BibleRoseData')
    if not BibleRoseDataDir:
        raise EnvironmentError("BibleRoseData environment variable is not set.")

    # Set files for English
    DictFile1 = BibleRoseDataDir +  "\\Dict\\SF_2009-01-20_ENG_KJV_(KJV+).BRdict.json"
    DictFile2 = BibleRoseDataDir +  "\\Dict\\SF_2009-01-22_ENG_RWEBSTER_(REVISED 1833 WEBSTER VERSION WITH STRONGS).BRdict.json"
    DictFileOut = BibleRoseDataDir +  "\\Dict\\ENG_COMBINE.BRdict.json"
    combine_dictionary_files(DictFile1, DictFile2, DictFileOut)

    # Set files for Greek stage 1
    DictFile1 = BibleRoseDataDir +  "\\Dict\\SF_2009-01-20_GRC_GNTWH_(WESTCOTT-HORT GREEK NEW TESTAMENT(STRONGS)).BRdict.json"
    DictFile2 = BibleRoseDataDir +  "\\Dict\\SF_2009-01-20_GRC_BZY2000_(BYZANTINE MAJORITY TEXT (2000 PLUS STRONGS)).BRdict.json"
    DictFileOut = BibleRoseDataDir +  "\\Dict\\GRC_COMBINE.BRdict.json"
    combine_dictionary_files(DictFile1, DictFile2, DictFileOut)

    # Set files for Greek stage 2
    DictFile1 = BibleRoseDataDir +  "\\Dict\\GRC_COMBINE.BRdict.json"
    DictFile2 = BibleRoseDataDir +  "\\Dict\\SF_2009-01-20_GRC_GNTTR_(TEXTUS RECEPTUS NT(STRONGS)).BRdict.json"
    DictFileOut = BibleRoseDataDir +  "\\Dict\\GRC_COMBINE.BRdict.json"
    combine_dictionary_files(DictFile1, DictFile2, DictFileOut)

