import pandas as pd
from load_data import load_data

#reshaping data from wide format to long

def clean_data(df):
    #striping whitespace
    df.columns = df.columns.str.strip()
    
    #dropping statewide total for the moment
    df = df.drop(columns=["Total"])

    #converting years to int
    df["Year"] = df["Year"].astype(int)

    #remove commas and converting county columsn to int
    county_columns = df.columns.drop("Year")
    for col in county_columns:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace(",","",regex=False)
            .astype(int)
        )

    #convert from wide to long
    long_df = df.melt(
        id_vars="Year",
        value_vars=county_columns,
        var_name="County",
        value_name="Crashes"
    )

    #Sort for clean analysis
    long_df = long_df.sort_values(["County", "Year"])

    return long_df

if __name__ == "__main__":
    df = load_data("data/raw/nj_crashes.csv")
    cleaned = clean_data(df)
    cleaned.to_csv("data/cleaned/cleaned_crashes.csv", index=False)
    print(cleaned.head())