import json
from collections import defaultdict, Counter
from BR_Extract_Verses import extract_verses

def build_strongs_dictionary(verse_strong):
    """
    Builds a dictionary of Strong's numbers to words, counting occurrences and considering case-insensitivity.
    """
    strongs_dict = defaultdict(lambda: defaultdict(int))  # {strongs_number: {word: count}}

    for verse, strongslist in verse_strong.items():
        for strongs, word in strongslist:
            # Normalize word to lowercase for comparison
            word_lower = word.lower()

            # Increase the frequency count of the word in the dictionary
            strongs_dict[strongs][word_lower] += 1

    # Now, for each Strong's number, store the most frequent word (case-sensitive)
    final_dict = {}
    for strongs_number, words in strongs_dict.items():
        # Sort words by frequency (highest first) and take the most common one
        most_common_word = max(words, key=words.get)
        
        # Store the most frequent word in its original case
        final_dict[strongs_number] = most_common_word

     # Sort Strong's numbers by alphabetic prefix and then numerically
    def sort_key(item):
        strongs = item[0]
        alpha_part = ''.join(filter(str.isalpha, strongs))
        numeric_part = int(''.join(filter(str.isdigit, strongs)))
        return (alpha_part, numeric_part)

    
    strongs_dict = dict(sorted(strongs_dict.items(), key=sort_key))

    final_dict = dict(sorted(final_dict.items(), key=sort_key))

    return final_dict


def write_strongs_dictionary(strongs_dict, output_file):
    """
    Writes the Strong's dictionary to a JSON file.
    """
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(strongs_dict, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    import os 

    BibleRoseDataDir = os.getenv('BibleRoseData')
    # Example usage:
    # verse_strong = extract_verses("your_file.xml")  # Assuming you've run the parsing script
    # strongs_dict = build_strongs_dictionary(verse_strong)
    print("Extracting verses from Zefania XML file...")
    #xml_file = BibleRoseDataDir + "\\SF_2009-01-20_GRC_GNTWH_(WESTCOTT-HORT GREEK NEW TESTAMENT(STRONGS)).xml"  # Update with actual filename
    #xml_file = BibleRoseDataDir + "\\SF_2009-01-20_GRC_GNTTR_(TEXTUS RECEPTUS NT(STRONGS)).xml"
    xml_file = BibleRoseDataDir + "\\SF_2009-01-20_ENG_KJV_(KJV+).xml"
    output_file = xml_file.rsplit(".xml", 1)[0] + ".BRdict.json"
    verse_strong = extract_verses(xml_file)
    print("Creating Stromgs Dictionary")
    strongs_dict = build_strongs_dictionary(verse_strong)
    write_strongs_dictionary(strongs_dict, output_file)
    print("Strong's dictionary saved successfully.")
