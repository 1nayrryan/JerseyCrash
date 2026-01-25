import pandas as pd

# encountered problems with missing columns
#current csv as of install was in wide format
#analysis requires long format, so we must reshape data

def load_data(path="data/cleaned/cleaned_crashes.csv"):
    df = pd.read_csv(path)

    df["Year"] = df["Year"].astype(int)
    df["Crashes"] = df["Crashes"].astype(int)
    return df

if __name__ == "__main__":
    df = load_data("data/raw/nj_crashes.csv")
    print(df.head())