import sqlite3
from sqlite_vec import serialize_float32
import json 
import math
from pathlib import Path


BASE_DIR = Path(__file__).parent  # current directory


# Start connection
conn = sqlite3.connect("hadith_embeddings.db")
cur = conn.cursor()

# Create Table 
cur.execute("""
CREATE TABLE IF NOT EXISTS hadiths (
    id INTEGER PRIMARY KEY,
    hadith_number INTEGER UNIQUE,
    chapter_number INTEGER,
    chapter_english TEXT,
    chapter_arabic TEXT,
    section_number INTEGER,
    section_english TEXT,
    section_arabic TEXT,
    english_hadith TEXT,
    english_isnad TEXT,
    english_matn TEXT,
    arabic_hadith TEXT,
    arabic_isnad TEXT,
    arabic_matn TEXT,
    arabic_comment TEXT,
    english_grade TEXT,
    arabic_grade TEXT,
    embeddings VECTOR(1536)
)
""")
conn.commit()

# Load JSON
with open(BASE_DIR / "../bukhari_GPT_embeddings_v2.json", "r", encoding="utf-8") as f:
    hadiths = json.load(f)

# Clean NaNs
for h in hadiths:
    for k, v in h.items():
        if isinstance(v, float) and math.isnan(v):
            h[k] = None

# Insert all rows in a loop
for h in hadiths:
    cur.execute("""
    INSERT OR REPLACE INTO hadiths (
        hadith_number, chapter_number, chapter_english, chapter_arabic,
        section_number, section_english, section_arabic,
        english_hadith, english_isnad, english_matn,
        arabic_hadith, arabic_isnad, arabic_matn, arabic_comment,
        english_grade, arabic_grade, embeddings
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        h["Hadith_number"],
        h["Chapter_Number"],
        h["Chapter_English"],
        h["Chapter_Arabic"],
        h["Section_Number"],
        h["Section_English"],
        h["Section_Arabic"],
        h["English_Hadith"],
        h["English_Isnad"],
        h["English_Matn"],
        h["Arabic_Hadith"],
        h["Arabic_Isnad"],
        h["Arabic_Matn"],
        h.get("Arabic_Comment"),
        h["English_Grade"],
        h["Arabic_Grade"],
        serialize_float32(h["embeddings"])
    ))

# Commit once at the end
conn.commit()
conn.close()

print("All Hadiths inserted safely.")