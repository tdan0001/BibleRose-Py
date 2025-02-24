import xml.etree.ElementTree as ET


def extract_verses(xml_file):
    """
    Parses a Zefania XML file and extracts verses in a dictionary format.
    """
    tree = ET.parse(xml_file)
    root = tree.getroot()

    verse_dict = {}
    verse_strong = {}

    # Iterate through the XML tree
    for book in root.findall(".//BIBLEBOOK"):  # <BIBLEBOOK bnumber="40" bname="Matthäus" bsname="Mt">
        book_name = book.get("bname")
        for chapter in book.findall("CHAPTER"):  # <CHAPTER cnumber="1">
            chapter_num = chapter.get("cnumber")
            for verse in chapter.findall("VERS"):  # <VERS vnumber="1">
                strongslist = []
                for greek in verse.findall("gr"):
                    strongs = greek.get("str")
                    word = greek.text.strip()
                    strongslist.append([strongs, word])
                verse_num = verse.get("vnumber")
              #  verse_text = "".join(verse.itertext())  # Extract text inside verse
                verse_ref = f"{book_name} {chapter_num}:{verse_num}"
               # verse_dict[verse_ref] = verse_text.strip()
                verse_strong[verse_ref] = strongslist

    return verse_strong


if __name__ == '__main__':
    # Example usage
    print("Extracting verses from Zefania XML file...")
    xml_file = "D:\\BibleDataXml\\SF_2009-01-20_GRC_GNTWH_(WESTCOTT-HORT GREEK NEW TESTAMENT(STRONGS)).xml"  # Update with actual filename
    verses = extract_verses(xml_file)

    # Print a sample
    for ref, text in list(verses.items())[:5]:  # Print first 5 verses
        print(f"{ref}: {text}")