import streamlit as st
import json
from BR_Extract_Verses_From_Zef import extract_verses_from_zef_url  # Replace with actual import
import os
import re
import requests

query_params = st.query_params
greek_selection = query_params.get("greek", "TR" ) 
basebible_selection = query_params.get("bible", "KJV" ) 

# Map of NT books
book_map = {
    "Matthew": 40,
    "Mark": 41,
    "Luke": 42,
    "John": 43,
    "Acts": 44,
    "Romans": 45,
    "1 Corinthians": 46,
    "2 Corinthians": 47,
    "Galatians": 48,
    "Ephesians": 49,
    "Philippians": 50,
    "Colossians": 51,
    "1 Thessalonians": 52,
    "2 Thessalonians": 53,
    "1 Timothy": 54,
    "2 Timothy": 55,
    "Titus": 56,
    "Philemon": 57,
    "Hebrews": 58,
    "James": 59,
    "1 Peter": 60,
    "2 Peter": 61,
    "1 John": 62,
    "2 John": 63,
    "3 John": 64,
    "Jude": 65,
    "Revelation": 66,
}

bibleUrls = {
    
    "WH" : ["GRE", "https://raw.githubusercontent.com/kohelet-net-admin/zefania-xml-bibles/refs/heads/master/Bibles/GRC/Westcott-Hort%20Greek%20NT/Strongs%20Numbers/SF_2009-01-20_GRC_GNTWH_(WESTCOTT-HORT%20GREEK%20NEW%20TESTAMENT(STRONGS)).xml"],
    "TR" : ["GRE", "https://raw.githubusercontent.com/kohelet-net-admin/zefania-xml-bibles/refs/heads/master/Bibles/GRC/Textus%20Receptus%20NT/Strongs%20Numbers/SF_2009-01-20_GRC_GNTTR_(TEXTUS%20RECEPTUS%20NT(STRONGS)).xml"],
    "BYZ" : ["GRE", "https://raw.githubusercontent.com/kohelet-net-admin/zefania-xml-bibles/refs/heads/master/Bibles/GRC/Byzantine/Majority%20Text%20(2000)/SF_2009-01-20_GRC_BZY2000_(BYZANTINE%20MAJORITY%20TEXT%20(2000%20PLUS%20STRONGS)).xml"],
    "Webster" : ["ENG", "https://raw.githubusercontent.com/kohelet-net-admin/zefania-xml-bibles/refs/heads/master/Bibles/ENG/Revised%201833%20Webster%20Version%20with%20Strongs/SF_2009-01-22_ENG_RWEBSTER_(REVISED%201833%20WEBSTER%20VERSION%20WITH%20STRONGS).xml"],
    "KJV" : ["ENG", "https://raw.githubusercontent.com/kohelet-net-admin/zefania-xml-bibles/refs/heads/master/Bibles/ENG/King%20James/KJV%2B/SF_2009-01-20_ENG_KJV_(KJV%2B).xml"],
    "RUS" : ["RUS", "https://raw.githubusercontent.com/kohelet-net-admin/zefania-xml-bibles/refs/heads/master/Bibles/RUS/Russian%20New%20Testament%20Strongs/SF_2009-01-20_RUS_RUSVZH_(RUSSIAN%20NEW%20TESTAMENT%20STRONGS).xml"],
    "Elberfelder" : ["GER", "https://raw.githubusercontent.com/kohelet-net-admin/zefania-xml-bibles/refs/heads/master/Bibles/GER/Elberfelder/Elberfelder%201905/SF_2009-01-22_GER_ELB1905STR_(ELBERFELDER%201905).xml"],
    "Luther" : ["GER", "https://github.com/kohelet-net-admin/zefania-xml-bibles/raw/refs/heads/master/Bibles/GER/Lutherbibel/Luther%201545%20mit%20Strongs/SF_2009-01-20_GER_LUTH1545STR_(LUTHER%201545%20MIT%20STRONGS).xml"],
    "Schlachterbibel" : ["GER", "https://github.com/kohelet-net-admin/zefania-xml-bibles/raw/refs/heads/master/Bibles/GER/Schlachterbibel/Schlachter%20Bibel%201951%20with%20Strong/SF_2009-01-20_GER_SCH1951_(SCHLACHTER%20BIBEL%201951%20WITH%20STRONG).xml"],
}


zef_url_greek = bibleUrls[greek_selection][1]
zef_url_base = bibleUrls[basebible_selection][1]
basebible_lang = bibleUrls[basebible_selection][0]
    
mainDictionaryUrl ="https://raw.githubusercontent.com/tdan0001/BibleRose-Py/refs/heads/master/BR_strongs_greek1.json"
st.cache_data()

# --- Load Greek Strong's data ---
@st.cache_data
def load_verse_data_greek():
    return extract_verses_from_zef_url(zef_url_greek, ".xml", True) 
greek_verses = load_verse_data_greek()

# --- Load English Bible  --
@st.cache_data
def load_verse_data_base(url):
    return extract_verses_from_zef_url(url, ".xml", False)
base_verses = load_verse_data_base(zef_url_base)


# --- Load BibleRose JSON file ---
@st.cache_data
def load_strongs_data():
    response = requests.get(mainDictionaryUrl)
    if response.status_code == 200:
         xml_string = response.text
         return json.loads(xml_string)
    else:
        BibleRoseDataDir = os.getenv('BibleRoseData')
        if not BibleRoseDataDir:
            raise EnvironmentError("BibleRoseData environment variable is not set.")
    
        #this file should be created by BR_Create_Main_Dictionary.py
        strongs_file = os.path.join(BibleRoseDataDir, "BR_strongs_greek1.json")
        if not os.path.exists(strongs_file):
            raise FileNotFoundError(f"Strong's data file not found: {strongs_file}")
    
        with open(strongs_file, "r", encoding="utf-8") as f:
            return json.load(f)
strongs_input = load_strongs_data()

strongs_data = strongs_input.get("Strongs", {})
# --- Streamlit UI ---
st.set_page_config(page_title="BibleRose Compare")
st.header("BibleRose Compare")
st.subheader("Compare Translations using Strongs Numbers")

# Verse selection
col1, col2, col3 = st.columns(3)
with col1:
    book_label = st.selectbox("Select Bible Book", list(book_map.keys()))
    book_number = book_map[book_label]
with col2:
    chapter = st.number_input("Chapter", min_value=1, value=1)
with col3:
    verse = st.number_input("Verse", min_value=1, value=1)

# Create reference key
verse_key = f"{book_number} {int(chapter)}:{int(verse)}"

# Get Greek strongs numbers from selected verse
greek_strongs = greek_verses.get(verse_key, [])

# Get Base Bible selected verse
base_verse = base_verses.get(verse_key, [])

# Lookup Base Bible equivalents from BibleRose JSON
def get_base_words(strongs_list):
    word_map = {}
    for sn in strongs_list:
        entry = strongs_data.get(sn)
        if entry and basebible_lang in entry:
            word_map[sn] = entry[basebible_lang]
    return word_map

# Show known base bible verse 


# User input
st.subheader("Paste Your Own Translation")
user_text = st.text_area("Enter a translation of the selected verse:")

if st.button("Compare Text") and user_text:
    base_words_map = get_base_words(greek_strongs)
    user_text_clean = re.sub(r"[.,;:!?()\[\]\"]", "", user_text)
    words = user_text_clean.split()

    matched_strongs = set()
    highlighted_text = []

    for word in words:
        match_found = False
        for sn, base_words in base_words_map.items():
            if word.lower() in [w.lower() for w in base_words]:
                highlighted_text.append(f"**:blue[{word}]**")
                matched_strongs.add(sn)
                match_found = True
                break
        if not match_found:
            highlighted_text.append(word)

    # Show Reference Translation
    st.subheader(basebible_selection + " (Reference Translation)")
    st.markdown(base_verse)
    
    # Show Greek Strong's numbers
    st.markdown("### Highlighted Pasted Text")
    st.markdown(" ".join(highlighted_text))

    # Unmatched Strong's numbers
    unmatched = set(greek_strongs) - matched_strongs
    if unmatched:
        st.markdown("### Unmatched Strong's Entries")
        for sn in unmatched:
            entry = strongs_data.get(sn)
            if entry:
                with st.expander(f" Strong's {sn}"):
                    st.markdown(f"**Definition:** {entry.get('Definition', '-')}")
                    st.markdown(f"**Words:** {', '.join(entry.get(basebible_lang, []))}")