import xml.etree.ElementTree as ET
import requests
import os
from collections import defaultdict
from BR_Parse_Strongs import parse_strongs_greek_xml
import json

def Add_Strongs_Words(mainDictionary, Language, AddedWords, source=None):
    """
    Adds word mappings to a master Strong's dictionary under the given language
    and optionally adds a source to the Sources list.

    Parameters:
        mainDictionary (dict): The master dictionary with full Strong's entries.
        Language (str): A language code such as "ENG", "FRE", "GER", etc.
        AddedWords (dict): Dictionary mapping Strong's numbers to word lists.
        source (str, optional): Source identifier (e.g., URL or file path).
    """

    # Add the source if it's not already present
    if source:
        if "Sources" not in mainDictionary:
            mainDictionary["Sources"] = []
        if source not in mainDictionary["Sources"]:
            mainDictionary["Sources"].append(source)

    for strongs_number, words in AddedWords.items():
        # Normalize Strong's key as integer: positive for G, negative for H, plain int otherwise
        strongs_trim = strongs_number.strip().upper()
        if strongs_trim.startswith("G"):
            strongs_index = int(strongs_trim[1:])
        elif strongs_trim.startswith("H"):
            strongs_index = -int(strongs_trim[1:])
        elif strongs_trim.isdigit():
            strongs_index = int(strongs_trim)
        else:
            strongs_index = 19999  # Default index for invalid Strong's numbers
            continue

        # Ensure the Strong's entry exists
        if "Strongs" not in mainDictionary:
            mainDictionary["Strongs"] = {}

        if strongs_index not in mainDictionary["Strongs"]:
            mainDictionary["Strongs"][strongs_index] = {
                "Definition": "",
                "Transliteration": "",
                "Pronunciation": "",
                "SeeAlso": "",
                "GRE":  [],
                "ENG":  [],
                "GER": [],
                "FRE": [],
                "SPA": [],
                "RUS": []
            }

        entry = mainDictionary["Strongs"][strongs_index]

        # Ensure language list exists
        if Language not in entry:
            entry[Language] = []

        # Add unique words
        existing_words = set(entry[Language])
        for word in words:
            if word not in existing_words:
                entry[Language].append(word)
                existing_words.add(word)


def load_strongs_dictionary(file_path):
    """
    Loads a Strong's dictionary from a JSON file.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

if __name__ == '__main__':
    BibleRoseDataDir = os.getenv('BibleRoseData')
    if not BibleRoseDataDir:
        raise EnvironmentError("BibleRoseData environment variable is not set.")

    url = "https://raw.githubusercontent.com/openscriptures/strongs/refs/heads/master/greek/StrongsGreekDictionaryXML_1.4/strongsgreek.xml"
    strongs_data = parse_strongs_greek_xml(url)

    engFiles =[
        BibleRoseDataDir + "\\Dict\\SF_2009-01-20_ENG_KJV_(KJV+).BRdict.json",
        BibleRoseDataDir + "\\Dict\\SF_2009-01-22_ENG_RWEBSTER_(REVISED 1833 WEBSTER VERSION WITH STRONGS).BRdict.json",
        ]

    for file in engFiles:
        if not os.path.exists(file):
            raise FileNotFoundError(f"File not found: {file}")
        engJson = load_strongs_dictionary(file)
        Add_Strongs_Words(strongs_data, "ENG", engJson, file)

    originalFiles =[
        BibleRoseDataDir +  "\\Dict\\SF_2009-01-20_GRC_GNTWH_(WESTCOTT-HORT GREEK NEW TESTAMENT(STRONGS)).BRdict.json",
        BibleRoseDataDir + "\\Dict\\SF_2009-01-20_GRC_BZY2000_(BYZANTINE MAJORITY TEXT (2000 PLUS STRONGS)).BRdict.json",
        BibleRoseDataDir +  "\\Dict\\SF_2009-01-20_GRC_GNTTR_(TEXTUS RECEPTUS NT(STRONGS)).BRdict.json"
        ]

    for file in originalFiles:
        if not os.path.exists(file):
            raise FileNotFoundError(f"File not found: {file}")
        engJson = load_strongs_dictionary(file)
        Add_Strongs_Words(strongs_data, "GRE", engJson, file)


    # Optional: save to JSON file
    with open(BibleRoseDataDir + "\\BR_strongs_greek1.json", "w", encoding="utf-8") as f:
        json.dump(strongs_data, f, ensure_ascii=False, indent=2)