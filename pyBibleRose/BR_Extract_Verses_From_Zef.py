import xml.etree.ElementTree as ET
import requests
import zipfile
import tempfile

def extract_verses_from_zef(xml_file, numbers_only=False):
    """
    Parses a Zefania XML file (or extracts from ZIP) and extracts verses in a dictionary format.
    Source files can be found at https://github.com/kohelet-net-admin/zefania-xml-bibles/tree/master
    """
    extracted_file = None

    # If the input file is a ZIP, extract the first XML file
    if xml_file.endswith(".zip"):
        with zipfile.ZipFile(xml_file, 'r') as zip_ref:
            xml_files = [f for f in zip_ref.namelist() if f.endswith(".xml")]
            if not xml_files:
                raise ValueError("No XML file found in the ZIP archive.")
            
            extracted_file = xml_files[0]  # Select the first XML file found
            with zip_ref.open(extracted_file) as xml_in_zip, tempfile.NamedTemporaryFile(delete=False, suffix=".xml") as temp_xml:
                temp_xml.write(xml_in_zip.read())
                temp_xml_path = temp_xml.name
            xml_file = temp_xml_path  # Use the temp file for parsing
    
    tree = ET.parse(xml_file)
    root = tree.getroot()

    verse_dict = {}
    verse_strong = {}

    # Iterate through the XML tree
    for book in root.findall(".//BIBLEBOOK"):  # <BIBLEBOOK bnumber="40" bname="Matth�us" bsname="Mt">
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

def extract_verses_from_zef_url(url, suffix = '.xml', numbers_only=False):
    """
    Downloads a Zefania XML file from a URL and extracts verses.
    """
    print("Extracting verses from Zefania URL: " + url)
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError(f"Failed to download file from {url}")
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
        temp_file.write(response.content)
        temp_file_path = temp_file.name
        verses = extract_verses_from_zef(temp_file_path, numbers_only)
    return verses


if __name__ == '__main__':
    # Example usage
    print("Extracting verses from Zefania XML file...")

    # Test case using a bible from a known repository
    zefURL = "https://sourceforge.net/projects/zefania-sharp/files/Bibles/ENG/Revised%201833%20Webster%20Version%20with%20Strongs/SF_2009-01-22_ENG_RWEBSTER_%28REVISED%201833%20WEBSTER%20VERSION%20WITH%20STRONGS%29.zip/download"
    verses = extract_verses_from_zef_url(zefURL, ".zip")
    
    #old test case using a local XML file
    # import os 
    # BibleRoseDataDir = os.getenv('BibleRoseData')
    # xml_file = BibleRoseDataDir + "\\SF_2009-01-20_GRC_GNTWH_(WESTCOTT-HORT GREEK NEW TESTAMENT(STRONGS)).xml"  # Update with actual filename
    # verses = extract_verses_from_zef(xml_file)

    # Print a sample
    for ref, text in list(verses.items())[:5]:  # Print first 5 verses
        print(f"{ref}: {text}")