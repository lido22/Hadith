import sqlite3
from sqlite_vec import serialize_float32
import sqlite_vec
import json
import time # Timing
from pathlib import Path # Standardizing Path
# Arabic printing
import arabic_reshaper 
from bidi.algorithm import get_display

BASE_DIR = Path(__file__).parent  # current directory


conn = sqlite3.connect("hadith_embeddings.db")
conn.row_factory = sqlite3.Row 

conn.enable_load_extension(True)
sqlite_vec.load(conn) 
conn.enable_load_extension(False)
cur = conn.cursor()

# Importing a hadith
with open(BASE_DIR / "../bukhari_GPT_embeddings_v2.json", "r", encoding="utf-8") as f:
    hadiths = json.load(f)

query_embedding = hadiths[4]['embeddings']
print("Hadith number: ", hadiths[4]['Hadith_number'])

# Wrap it using serialize_float32
query_blob = serialize_float32(query_embedding)

start = time.time()
# Query top 5 nearest neighbors
cur.execute("""
SELECT hadith_number, chapter_arabic, section_arabic, arabic_matn,
       vec_distance_cosine(embeddings, ?) AS distance
FROM hadiths
ORDER BY distance ASC
LIMIT 5
""", (query_blob,))
results = cur.fetchall()
end = time.time()
print(f"Query executed in {(end - start)*1000:.3f} milliseconds")

# Display
for r in results:
    chapter_arabic = get_display(arabic_reshaper.reshape(r['chapter_arabic']))
    section_arabic = get_display(arabic_reshaper.reshape(r['section_arabic']))
    arabic_matn = get_display(arabic_reshaper.reshape(r['arabic_matn']))
    print(f"Hadith #{r['hadith_number']} | Chapter: {chapter_arabic} | Section: {section_arabic}")
    print(arabic_matn[:200] + "…")  # first 200 chars
    print("-" * 80)

conn.close()