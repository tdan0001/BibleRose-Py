import json
from collections import defaultdict, Counter
from BR_Extract_Verses import extract_verses

def build_strongs_dictionary(verse_strong):
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

     # Sort Strong's numbers in ascending order
    strongs_dict = dict(sorted(strongs_dict.items(), key=lambda x: int(x[0][1:])))  # Sort numerically

    return strongs_dict


def write_strongs_dictionary(strongs_dict, output_file):
    """
    Writes the Strong's dictionary to a JSON file.
    """
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(strongs_dict, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    # Example usage:
    # verse_strong = extract_verses("your_file.xml")  # Assuming you've run the parsing script
    # strongs_dict = build_strongs_dictionary(verse_strong)
    print("Extracting verses from Zefania XML file...")
    xml_file = "D:\\BibleDataXml\\SF_2009-01-20_GRC_GNTWH_(WESTCOTT-HORT GREEK NEW TESTAMENT(STRONGS)).xml"  # Update with actual filename
    verse_strong = extract_verses(xml_file)
    print("Creating Stromgs Dictionary")
    strongs_dict = build_strongs_dictionary(verse_strong)
    write_strongs_dictionary(strongs_dict, "strongs_dict.json")
    print("Strong's dictionary saved successfully.")
