from pathlib import Path
from typing import Iterator
import polars as pl


TASHKEEL_PATTERN = r'[\u064B-\u065F\u0610-\u061A\u06D6-\u06ED]'

INVISIBLE_CHARS_PATTERN = r'[\u200e\u061c\u200f\u200b\u200c\u200d\ufeff]'

WHITE_SPACE_PATTERN = r'[\u0020\u00A0\u1680\u2000-\u200A\u202F\u205F\u3000]+'

HONORIFICS_PATTERN = r'صلى الله عليه وسلم|عليه الصلاة والسلام|رضي الله عنه|رضي الله عنها|رضي الله عنهم|عز وجل'

def iter_hadith_dataframes(data_dir: str) -> Iterator[pl.DataFrame]:

    for csv_file in Path(data_dir).glob("*.csv"):

        lf = (
            pl.scan_csv(csv_file, infer_schema_length=1000)
            .select(["Chapter_Arabic", "Hadith_number", "Arabic_Isnad", "Arabic_Matn", "Arabic_Grade"])
            .drop_nulls(subset=["Arabic_Matn"])
            .with_columns(
                pl.col("Arabic_Matn")
                .str.replace_all(TASHKEEL_PATTERN, '')
                .str.replace_all(INVISIBLE_CHARS_PATTERN, '')
                .str.replace_all(HONORIFICS_PATTERN, '')
                .str.replace_all(WHITE_SPACE_PATTERN, ' ')
            )
        )

        yield lf.collect()
