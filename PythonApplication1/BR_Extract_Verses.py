import xml.etree.ElementTree as ET


def extract_verses(xml_file, numbers_only=False):
    """
    Parses a Zefania XML file (or extracts from ZIP) and extracts verses in a dictionary format.
    """
    extracted_file = None

    # If the input file is a ZIP, extract the first XML file
    if xml_file.endswith(".zip"):
        with zipfile.ZipFile(xml_file, 'r') as zip_ref:
            xml_files = [f for f in zip_ref.namelist() if f.endswith(".xml")]
            if not xml_files:
                raise ValueError("No XML file found in the ZIP archive.")
            
            extracted_file = xml_files[0]  # Select the first XML file found
            zip_ref.extract(extracted_file)  # Extract it to the current directory
            xml_file = extracted_file  # Update the filename to parse

    tree = ET.parse(xml_file)
    root = tree.getroot()

    verse_dict = {}
    verse_strong = {}

    # Iterate through the XML tree
    for book in root.findall(".//BIBLEBOOK"):  # <BIBLEBOOK bnumber="40" bname="Matthäus" bsname="Mt">
        book_name = book.get("bnumber")
        for chapter in book.findall("CHAPTER"):  # <CHAPTER cnumber="1">
            chapter_num = chapter.get("cnumber")
            for verse in chapter.findall("VERS"):  # <VERS vnumber="1">
                strongslist = []
                for greek in verse.findall("gr"):
                    strongs = greek.get("str")
                    word = greek.text.strip() if greek.text else " "
                    if numbers_only:
                        if not(strongslist.__contains__(strongs)) :
                            strongslist.append(strongs)
                    else:
                        strongslist.append([strongs, word])
                verse_num = verse.get("vnumber")
              #  verse_text = "".join(verse.itertext())  # Extract text inside verse
                verse_ref = f"{book_name} {chapter_num}:{verse_num}"
               # verse_dict[verse_ref] = verse_text.strip()
                verse_strong[verse_ref] = strongslist

    return verse_strong


if __name__ == '__main__':
    import os 

    BibleRoseDataDir = os.getenv('BibleRoseData')


    # Example usage
    print("Extracting verses from Zefania XML file...")
    xml_file = BibleRoseDataDir + "\\SF_2009-01-20_GRC_GNTWH_(WESTCOTT-HORT GREEK NEW TESTAMENT(STRONGS)).xml"  # Update with actual filename
    verses = extract_verses(xml_file)

    # Print a sample
    for ref, text in list(verses.items())[:5]:  # Print first 5 verses
        print(f"{ref}: {text}")