import pandas as pd

df = pd.read_csv("data/cleaned/cleaned_crashes.csv")

print(df.dtypes)
print(df.isna().sum())
print(df.groupby("County")["Year"].count().head())


#average crashes per county
avg_crashes = (
    df.groupby("County")["Crashes"]
    .mean()
    .sort_values(ascending=False)
)

def year_over_year_change(df):
    df = df.sort_values(["County", "Year"])
    df["yoy_change"] = df.groupby("County")["Crashes"].diff()
    return df


yearly_totals = (
    df.groupby("Year")["Crashes"]
    .sum()
    .reset_index()
)

# #2020 Crash comparison, since datas are relevant up to the year 2020
def covid_impact(df):
    pre = df[df["Year"] == 2019].groupby("County")["Crashes"].sum()
    post = df[df["Year"] == 2020].groupby("County")["Crashes"].sum()

    impact = ((post - pre) / pre * 100).sort_values()
    return impact

yoy = year_over_year_change(df)
covid = covid_impact(df)

avg_crashes.to_csv("output/summaries/avg_crashes_by_county.csv")
yearly_totals.to_csv("output/summaries/avg_growth_by_county.csv")
covid.to_csv("output/summaries/covid_impact.csv")
yoy.to_csv("output/summaries/yoy_changes.csv")

print("Analysis complete. Results saved.")