import xml.etree.ElementTree as ET
import requests
import zipfile
import tempfile

def extract_verses_from_osis(xml_file, numbers_only=False):
    """
    Parses an OSIS XML file and extracts verses with Strong's numbers.
    Returns a dictionary: { "Book Chapter:Verse": [[strongs_number, word], ...], ... }
    """
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
    ns = {'osis': 'http://www.bibletechnologies.net/2003/OSIS/namespace'}  # Adjust if your OSIS uses a different namespace

    verse_strong = {}

    for verse in root.findall('.//osis:verse', ns):
        ref = verse.get('osisID')  # e.g., "Matt.1.1"
        if not ref:
            continue
        strongslist = []
        for w in verse.findall('.//osis:w', ns):
            lemma = w.get('lemma', '')
            word = w.text.strip() if w.text else ''
            # Extract Strong's numbers from lemma attribute
            strongs_numbers = [s for s in lemma.split() if s.startswith('strong:')]
            for strong in strongs_numbers:
                strong_num = strong.split(':')[1]
                if numbers_only:
                    if strong_num not in strongslist:
                        strongslist.append(strong_num)
                else:
                    strongslist.append([strong_num, word])
        verse_strong[ref] = strongslist

    return verse_strong

def extract_verses_from_oasis_url(url, suffix = '.xml', numbers_only=False):
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
        verses = extract_verses_from_osis(temp_file_path, numbers_only)
    return verses

if __name__ == '__main__':
    # Example usage
    print("Extracting verses from Zefania XML file...")

    osisZip = "https://www2.crosswire.org/ftpmirror/pub/sword/packages/rawzip/FreJND.zip"
    verses = extract_verses_from_oasis_url(osisZip, ".zip")
    
    #old test case using a local XML file
    # import os 
    # BibleRoseDataDir = os.getenv('BibleRoseData')
    # xml_file = BibleRoseDataDir + "\\SF_2009-01-20_GRC_GNTWH_(WESTCOTT-HORT GREEK NEW TESTAMENT(STRONGS)).xml"  # Update with actual filename
    # verses = extract_verses_from_zef(xml_file)

    # Print a sample
    for ref, text in list(verses.items())[:5]:  # Print first 5 verses
        print(f"{ref}: {text}")