import xml.etree.ElementTree as ET
import requests
import os
from collections import defaultdict

def parse_strongs_greek_xml(url):
    """
    Parses the Strong's Greek XML file from the given URL and returns a structured dictionary.
    """
    response = requests.get(url)
    response.raise_for_status()  # Will throw error if fetch fails

    root = ET.fromstring(response.content)

    strongs_dict = defaultdict(dict)

    # Upper Levels of the XML, Most datea wil go under "Strongs"
    source_data = {
        "Strongs": strongs_dict,
        "Sources": [url],
        "Original": "Greek"
    }

    entries = root.find("entries").findall("entry")
    for entry in entries:

        strongs_number = entry.attrib.get("strongs")
        strongs_key = int(strongs_number)  # strips leading 0's

        # Text fields with possible missing tags
        definition = entry.findtext("strongs_def", default="").strip().replace("\n", " ")
        derivation = entry.findtext("strongs_derivation", default="").strip()
        kjv_def = entry.findtext("kjv_def", default="").strip().replace("\n", " ").replace(":--", "").replace(".", ".  ")


        # Handle sub-elements
        greek_elem = entry.find("greek")
        greek = greek_elem.attrib.get("unicode", "").strip() if greek_elem is not None else ""
        translit = greek_elem.attrib.get("translit", "").strip() if greek_elem is not None else ""

        pronunciation_elem = entry.find("pronunciation")
        pronunciation = pronunciation_elem.attrib.get("strongs", "").strip() if pronunciation_elem is not None else ""

        # SeeAlso references
        see_refs = [see.attrib.get("strongs") for see in entry.findall("see")]

        # Build entry
        strongs_dict[strongs_key] = {
            "Definition": kjv_def + definition,
            "Transliteration": translit,
            "Pronunciation": pronunciation,
            "SeeAlso": see_refs,
            "GRE": [greek] if greek else [],
            "ENG": [],
            "GER": [],
            "FRE": [],
            "SPA": [],
            "RUS": []
        }

    return source_data


if __name__ == "__main__":
    # Unit Testing code, actual run is done in BR_Create_Main_Dictionary.py
    BibleRoseDataDir = os.getenv('BibleRoseData')
    if not BibleRoseDataDir:
        raise EnvironmentError("BibleRoseData environment variable is not set.")

    url = "https://raw.githubusercontent.com/openscriptures/strongs/refs/heads/master/greek/StrongsGreekDictionaryXML_1.4/strongsgreek.xml"
    strongs_data = parse_strongs_greek_xml(url)

    # Optional: save to JSON file
    import json
    with open(BibleRoseDataDir + "\\BR_strongs_greek.json", "w", encoding="utf-8") as f:
        json.dump(strongs_data, f, ensure_ascii=False, indent=2)