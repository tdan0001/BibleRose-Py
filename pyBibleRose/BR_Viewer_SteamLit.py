import streamlit as st
import json
from BR_Extract_Verses_From_Zef import extract_verses_from_zef_url  # Replace with actual import
import os
import requests


# --- Book map for combo box ---
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

# --- Load Greek Strong's data ---
zef_url = "https://raw.githubusercontent.com/kohelet-net-admin/zefania-xml-bibles/refs/heads/master/Bibles/GRC/Westcott-Hort%20Greek%20NT/Strongs%20Numbers/SF_2009-01-20_GRC_GNTWH_(WESTCOTT-HORT%20GREEK%20NEW%20TESTAMENT(STRONGS)).xml"
mainDictionaryUrl ="https://raw.githubusercontent.com/tdan0001/BibleRose-Py/refs/heads/master/BR_strongs_greek1.json"
st.cache_data()

@st.cache_data
def load_verse_data():
    return extract_verses_from_zef_url(zef_url, ".xml", True)
greek_verses = load_verse_data()

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

# --- UI ---
st.header("BibleRose Viewer")
st.subheader("Verse to Strong's Dictionary")

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

# --- Populate Strong's number box ---
default_strongs = greek_verses.get(verse_key, [])
default_strongs_text = ", ".join(default_strongs)

strongs_input = st.text_input("Strong's Numbers (editable)", value=default_strongs_text)

if st.button("Get Entries"):
    entered_strongs = [s.strip() for s in strongs_input.split(",") if s.strip()]

    if not entered_strongs:
        st.warning("Please enter one or more Strong's numbers.")
    else:
        for strongs_num in entered_strongs:
            entry = strongs_data.get(strongs_num)
            if entry:
                with st.expander(f":blue[Strongs] {strongs_num}"):
                    st.markdown(f":blue[**Definition:**] {entry.get('Definition', '-')}")
                    st.markdown(f":blue[**Transliteration:**] {entry.get('Transliteration', '-')}")
                    st.markdown(f":blue[**Pronunciation:**] {entry.get('Pronunciation', '-')}")

                    for lang in ["GRE", "ENG", "GER", "FRE", "SPA", "RUS", "zh-Hant", "zh-Hans", "nl", "Arabic"]:
                        if lang in entry:
                            st.markdown(f":blue[**{lang}:**] {', '.join(entry[lang])}")
            else:
                st.warning(f"No entry found for Strong's {strongs_num}")
