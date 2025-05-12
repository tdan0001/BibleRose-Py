import json

def extract_strongs_from_greek(verse_strong_data):
    """
    Extracts Strong's numbers from a given Greek verse.
    :param verse_strong_data: Dictionary of verse references to Strong's numbers and words.
    :return: List of Strong's numbers in the verse.
    """
    strongs_numbers = []
    for entry in verse_strong_data:
        strongs_numbers.append(entry[0])  # Extract Strong's number
    return strongs_numbers

def get_english_words(strongs_numbers, strongs_dict):
    """
    Retrieves the English words associated with a list of Strong's numbers.
    :param strongs_numbers: List of Strong's numbers.
    :param strongs_dict: Dictionary mapping Strong's numbers to English words.
    :return: Dictionary of Strong's numbers to associated English words.
    """
    words_map = {}
    for strongs in strongs_numbers:
        if strongs in strongs_dict:
            words_map[strongs] = strongs_dict[strongs]
    return words_map

def compare_with_english_translation(english_text, words_map):
    """
    Compares the extracted Strong’s words with an English verse translation.
    Highlights matched and missing words.
    :param english_text: The verse text from the English translation.
    :param words_map: Dictionary of Strong's numbers to English words.
    :return: Dictionary categorizing words as 'matched' or 'missing'.
    """
    english_words = english_text.lower().split()
    matched = {}
    missing = {}

    for strongs, words in words_map.items():
        found = any(word.lower() in english_words for word in words)
        if found:
            matched[strongs] = words
        else:
            missing[strongs] = words

    return {"matched": matched, "missing": missing}

# Example Data
verse_reference = "John 1:1"
greek_verse_strongs = [["G1722", "ἐν"], ["G746", "ἀρχῇ"], ["G2258", "ἦν"], ["G3588", "ὁ"], ["G3056", "λόγος"]]

strongs_dict = {
    "G1722": ["in"],
    "G746": ["beginning"],
    "G2258": ["was"],
    "G3588": ["the"],
    "G3056": ["word"]
}

english_translation = "In the beginning was the Word."

# Process
strongs_numbers = extract_strongs_from_greek(greek_verse_strongs)
words_map = get_english_words(strongs_numbers, strongs_dict)
comparison_result = compare_with_english_translation(english_translation, words_map)

# Output
print(f"Verse: {verse_reference}")
print("Matched Words:", comparison_result["matched"])
print("Missing Words:", comparison_result["missing"])