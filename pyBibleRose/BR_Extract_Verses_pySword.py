import pysword
import re
from collections import defaultdict
from pysword.modules import SwordModules
from BR_Add_Words import Add_Strongs_Words


def parse_strongs_from_pysword(xml_string):
    """
    Parses Strong's words from a given XML string and returns a dictionary mapping Strong's numbers to lists of words.
    """
    strongs_data = defaultdict(list)  # {strong_number: [words]}

    # Find all <w lemma="strong:G####">Text</w>
    matches = re.findall(r'<w lemma="strong:([GH]\d+)">(.*?)</w>', xml_string)

    for strong_num, word in matches:
        if not strongs_data[strong_num].__contains__(word):
            strongs_data[strong_num].append(word)
    
    return strongs_data

def add_strongs_from_sword(mainDictionary):
    """
    Adds Strong's words from Sword modules to the main dictionary.
    mainDictionary - The main dictionary to which Strong's words will be added.
    """
    modules = SwordModules()
    found_modules = modules.parse_modules() # not sure if the output is needed, but the call is required to load the modules
    newTestamentBooks = ['Matt', 'Mark', 'Luke', 'John', 'Acts', 'Rom', '1Cor', '2Cor', 'Gal', 'Eph', 'Phil', 'Col', '1Thess', '2Thess', '1Tim', '2Tim', 'Titus', 'Phlm', 'Hebrews', 'Jas', '1Pet', '2Pet', '1John', '2John', '3John', 'Jude', 'Rev'];

    for mod in modules._modules:
        try:
            print("Processing Sword module: " + mod)
            modx = modules._modules[mod]  #gets the metadata for the module
            modLang = modx['lang']
            if modLang == "en": modLang = "ENG"
            if modLang == "fr": modLang = "FRE"
            if modLang == "es": modLang = "SPA"
            if modLang == "grc": modLang = "GRE"
            if modLang == "ru": modLang = "RUS"
            if modLang == "de": modLang = "GER"

            bible = modules.get_bible_from_module(mod) # gets the actual bible test from the module
            output = bible.get(books=newTestamentBooks, clean=False)

            strongs_data = parse_strongs_from_pysword(output)
            Add_Strongs_Words(mainDictionary, modLang, strongs_data, source="SwordModule:"+mod)
        except Exception as e:
            print(f"Error processing module: {e}")  # mostly catches bibles that dont have a new testament 
            continue


if __name__ == '__main__':
    # Example unit testing usage
    
    # Find available modules/bibles in standard data path.
    # For non-standard data path, pass it as an argument to the SwordModules constructor.
    modules = SwordModules()
    found_modules = modules.parse_modules()
    bible = modules.get_bible_from_module(u'RV_th')

    newTestamentBooks = ['Matt', 'Mark', 'Luke', 'John', 'Acts', 'Rom', '1Cor', '2Cor', 'Gal', 'Eph', 'Phil', 'Col', '1Thess', '2Thess', '1Tim', '2Tim', 'Titus', 'Phlm', 'Hebrews', 'Jas', '1Pet', '2Pet', '1John', '2John', '3John', 'Jude', 'Rev'];

    output = bible.get(books=newTestamentBooks, clean=False)
    strongs_data = parse_strongs_from_pysword(output)

    print (strongs_data)

    # Following Sword modules were loaded at time of testing as they contained strongs numbers:
    # ABP, abpen_sb, abpgk_sb, ABPGRK, Antoniades, Byz, ChiUn, ChiUns, CzeCSP, Darby, deu1912eb, 
    # DutSVVA, Elzevir, engASV1901eb, engasvbt2021eb, engBBE1964eb, engbsb2020eb, engDBY1884eb, engDRA1899eb, 
    # engerv2006eb, engf35eb, engfbv2018eb, engGLW1996eb, engKJV1769eb, engKJV2006eb, englsv2020eb, engNET2016eb, 
    # engoebcweb, engoebuseb, engPEV2019eb, engRV1895eb, engT4T2014eb, engtcent2022eb, engweb2025eb, engweb2025peb, 
    # engwebbe2025eb, engwebbe2025peb, engwebc2025eb, engwebu2025eb, engwebuk2024eb, engwmb2025eb, engwmbb2025eb, 
    # fraFOB1744eb, fraLSG1910eb, francl2022eb, frasbl2022eb, FreJND, GerLeoNA28, GerLeoRP18, GerSch, grctreb,
    # KJVA, MorphGNT, NASB, RLT, RusSynodalLIO, RusVZh, RV_th, RWebster, SBLG_th, spaBES2018eb, spablm2022eb, 
    # spapddpt2022eb, SpaRV, spaRV1909eb, sparvg2010eb, SpaTDP, spav1602peb, spavbl2018eb, StatResGNT, Tisch, TischMorph, TR, WHNU


