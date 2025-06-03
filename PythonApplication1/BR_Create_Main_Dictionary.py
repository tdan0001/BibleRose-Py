import json
import os
from collections import defaultdict, Counter
from BR_Build_Strongs_Words_From_Zef import build_strongs_words_from_zef
from BR_Parse_Strongs import parse_strongs_greek_xml
from BR_Add_Words import Add_Strongs_Words
from BR_Extract_Verses_From_Zef import extract_verses_from_zef_url

def create_main_dictionary():


    # Parse the Strong's Greek XML file
    url = "https://raw.githubusercontent.com/openscriptures/strongs/refs/heads/master/greek/StrongsGreekDictionaryXML_1.4/strongsgreek.xml"
    strongs_data = parse_strongs_greek_xml(url)

    # Add Greek words from Zefania XML files
    zefRoot = "https://raw.githubusercontent.com/kohelet-net-admin/zefania-xml-bibles/refs/heads/master/Bibles/GRC"
    zefFiles =[
        zefRoot +  "/Westcott-Hort%20Greek%20NT/Strongs%20Numbers/SF_2009-01-20_GRC_GNTWH_(WESTCOTT-HORT%20GREEK%20NEW%20TESTAMENT(STRONGS)).xml",
        zefRoot + "/Textus%20Receptus%20NT/Strongs%20Numbers/SF_2009-01-20_GRC_GNTTR_(TEXTUS%20RECEPTUS%20NT(STRONGS)).xml",
        zefRoot +  "/Byzantine/Majority%20Text%20(2000)/SF_2009-01-20_GRC_BZY2000_(BYZANTINE%20MAJORITY%20TEXT%20(2000%20PLUS%20STRONGS)).xml",
        ]
    add_words_from_url(strongs_data, zefFiles, "Original")

    
    # Add English words from Zefania XML files
    zefRoot = "https://raw.githubusercontent.com/kohelet-net-admin/zefania-xml-bibles/refs/heads/master/Bibles/ENG"
    zefFiles =[
        zefRoot + "/Revised%201833%20Webster%20Version%20with%20Strongs/SF_2009-01-22_ENG_RWEBSTER_(REVISED%201833%20WEBSTER%20VERSION%20WITH%20STRONGS).xml",
        zefRoot + "/King%20James/KJV%2B/SF_2009-01-20_ENG_KJV_(KJV%2B).xml",
        ]
    add_words_from_url(strongs_data, zefFiles, "ENG")

    zefFiles =[ "https://raw.githubusercontent.com/kohelet-net-admin/zefania-xml-bibles/refs/heads/master/Bibles/RUS/Russian%20New%20Testament%20Strongs/SF_2009-01-20_RUS_RUSVZH_(RUSSIAN%20NEW%20TESTAMENT%20STRONGS).xml"]
    add_words_from_url(strongs_data, zefFiles, "RUS")

    zefFiles =[ "https://raw.githubusercontent.com/kohelet-net-admin/zefania-xml-bibles/refs/heads/master/Bibles/GER/Elberfelder/Elberfelder%201905/SF_2009-01-22_GER_ELB1905STR_(ELBERFELDER%201905).xml",
               "https://github.com/kohelet-net-admin/zefania-xml-bibles/raw/refs/heads/master/Bibles/GER/Lutherbibel/Luther%201545%20mit%20Strongs/SF_2009-01-20_GER_LUTH1545STR_(LUTHER%201545%20MIT%20STRONGS).xml",
               "https://github.com/kohelet-net-admin/zefania-xml-bibles/raw/refs/heads/master/Bibles/GER/Schlachterbibel/Schlachter%20Bibel%201951%20with%20Strong/SF_2009-01-20_GER_SCH1951_(SCHLACHTER%20BIBEL%201951%20WITH%20STRONG).xml"]
    add_words_from_url(strongs_data, zefFiles, "GER")
    return strongs_data

def add_words_from_url(mainDictionary, urls, Language):
    """
    Adds words from a URL to the main dictionary under the specified language.
    """
    for url in urls:
        verse_strong = extract_verses_from_zef_url(url)
        strongs_data = build_strongs_words_from_zef(verse_strong)
        Add_Strongs_Words(mainDictionary, Language, strongs_data, url)


if __name__ == "__main__":
    strongs_data = create_main_dictionary()


    BibleRoseDataDir = os.getenv('BibleRoseData')
    if not BibleRoseDataDir:
        raise EnvironmentError("BibleRoseData environment variable is not set.")
    # Save to JSON file
    with open(BibleRoseDataDir + "\\BR_strongs_greek1.json", "w", encoding="utf-8") as f:
        json.dump(strongs_data, f, ensure_ascii=False, indent=2)
