from hadith_loader import iter_hadith_dataframes 


HADITH_DATA_DIR = "data"

def main():
    for df in iter_hadith_dataframes(HADITH_DATA_DIR):
        print(df.head(1))

if __name__ == "__main__":
    main()