# BibleRose (In Development)
**A multi-version Bible study tool inspired by the Rosetta Stone.**  
BibleRose uses **Strong’s Numbers** and **XML-based verse mapping** to visualize word usage across different Bible translations.

The name reflects the goal: unlocking cross-language understanding through layered comparison.

## Current Status:
BibleRose is currently a **Python-based backend project**.  
It uses [`pySword`](https://github.com/karlkleinpaste/jsword) to read some of Bible modules and extract structured text and metadata.


## Planned Features:
- Remove repetition from Strong’s-based language dictionaries
- Build a visual comparison tool to explore translation differences

> Main script: `BR_Create_Main_Dictionary.py`

Each entry maps a Strong’s number to its multilingual equivalents and linguistic metadata:
## Sample Output Snippet:
```json
  "320": {
    "Definition": "reading.  (the act of) reading",
    "Transliteration": "anágnōsis",
    "Pronunciation": "an-ag'-no-sis",
    "SeeAlso": ["314"],
    "GRE": ["ἀνάγνωσις", "αναγνωσει", "αναγνωσιν", "ἀνάγνωσιν", "ἀναγνώσει", "ἀναγνώσει,"],
    "ENG": ["reading", "latter", "read", "the reading", "to the public reading of scripture"],
    "GER": ["Vorlesen", "zeugte", "Lesen", "künftigen", "Lektion", "lesen"],
    "FRE": ["lecture"],
    "SPA": ["lectura", "la lección", "en leer"],
    "RUS": ["чтением", "чтения", "чтении"],
    "zh-Hant": ["讀", "誦讀", "你要以宣讀"],
    "zh-Hans": ["读", "诵读", "你要以宣读"],
    "nl": ["lezen"]
  }
```
This shows how a single Greek Strong’s number (G320) connects to equivalent words and phrases across multiple translations and languages.

