import colorama
from colorama import Fore, Style

# Initialize colorama
colorama.init(autoreset=True)


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



def colorize_word(word, match_type):
    """Assigns color based on match type."""
    colors = {
        "Minor": Fore.BLUE,        # Exact match
        "MinorX": Fore.CYAN,       # Slight difference
        "Strong": Fore.WHITE,     # Significant match
        "StrongX": Fore.YELLOW,    # Significant difference
        "unused": Fore.RED          # Strong's number not found in translation
    }
    return f"{colors.get(match_type, Fore.WHITE)}{word}{Style.RESET_ALL}"

def compare_translations(greek_text, strongs_dict, english1, english2=None):
    """Compares Greek text with one or two English translations and highlights differences."""
    for verse_ref, greek_words in greek_text.items():
        print(f"\n{Fore.WHITE}{verse_ref}{Style.RESET_ALL}")
        
        used_strongs = set()
        
        # Display first English translation
        print("English 1:")
        for word in english1.get(verse_ref, "").split():
            match_type = "match" if word.lower() in strongs_dict else "unused"
            print(colorize_word(word, match_type), end=" ")
        print("\n")


def view_translation(target_verse,greek_strongs,target_dictionary):
    # Display first English translation

    print("English 1:")
    for word in target_verse:
        match_type = "Strong" if word.lower() in target_dictorary else "Minor"
        print(colorize_word(word, match_type), end=" ")
    print("\n")
      

def main():



    # Sample Data (Replace with actual parsed data)
    greek_text = {
        "John 1:1": [("G3056", "λόγος"), ("G1510", "ἦν"), ("G2316", "θεός")]
    }
    strongs_dict = {
        "G3056": "word",
        "G1510": "was",
        "G2316": "God"
    }
    english1 = {
        "John 1:1": "In the beginning was the Word, and the Word was with God, and the Word was God."
    }
    english2 = {
        "John 1:1": "At the start was the Word, and the Word was alongside God, and the Word was truly God."
    }

    greek_strongs = extract_strongs_from_greek(greek_text)
    target_dictionary = get_english_words(greek_strongs, strongs_dict)
    view_translation(english1,greek_strongs,target_dictionary)
    
    compare_translations(greek_text, strongs_dict, english1, english2)

if __name__ == "__main__":
    main()