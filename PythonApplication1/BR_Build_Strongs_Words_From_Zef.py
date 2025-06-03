import json
import os
from collections import defaultdict, Counter
from BR_Extract_Verses_From_Zef import extract_verses_from_zef

def build_strongs_words_from_zef(verse_strong):
    """
    Creates a dictionary mapping Strong's numbers to words, sorted by frequency.
    """
    strongs_dict = defaultdict(list)
    word_counts = defaultdict(Counter)

    # Build frequency data
    for verse, words in verse_strong.items():
        for strongs, word in words:
            word_counts[strongs][word] += 1

    # Convert to dictionary with sorted words
    for strongs, counter in word_counts.items():
        strongs_dict[strongs] = [word for word, _ in counter.most_common()]

    # Sort Strong's numbers by alphabetic prefix and then numerically
    def sort_key(item):
        strongs = item[0]
        alpha_part = ''.join(filter(str.isalpha, strongs))
        numeric_part = int(''.join(filter(str.isdigit, strongs)))
        return (alpha_part, numeric_part)

    strongs_dict = dict(sorted(strongs_dict.items(), key=sort_key))

    return strongs_dict

def write_strongs_dictionary(strongs_dict, output_file):
    """
    Writes the Strong's dictionary to a JSON file.
    """
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(strongs_dict, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    BibleRoseDataDir = os.getenv('BibleRoseData')
    if not BibleRoseDataDir:
        raise EnvironmentError("BibleRoseData environment variable is not set.")

    # Get all XML files in the directory
    xml_files = [f for f in os.listdir(BibleRoseDataDir) if f.endswith('.xml')]

    for xml_file in xml_files:
        full_path = os.path.join(BibleRoseDataDir, xml_file)
        output_file = full_path.rsplit(".xml", 1)[0] + ".BRdict.json"
        print(f"Processing {xml_file}...")
        verse_strong = extract_verses_from_zef(full_path)
        print("Creating Strong's Dictionary")
        strongs_dict = build_strongs_words_from_zef(verse_strong)
        write_strongs_dictionary(strongs_dict, output_file)
        print(f"Strong's dictionary for {xml_file} saved successfully.")
