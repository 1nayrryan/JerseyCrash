import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import pandas as pd

def plot_top_counties(df, top_n=5):
    avg = (
        df.groupby("County")["Crashes"]
        .mean()
        .sort_values(ascending=False)
        .head(top_n)
    )

    avg.plot(kind="bar")
    plt.title("Top Counties by Average Crash Count")
    plt.ylabel("Average Crashes")
    plt.tight_layout()
    plt.savefig("output/charts/top_counties.png")
    plt.close()

def plot_yearly_trend(df):
    yearly = df.groupby("Year")["Crashes"].sum()
    ax = yearly.plot(x="Year", y="Crashes")
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))


    yearly.plot()
    plt.title("NJ Traffic Crashes Over Time")
    plt.ylabel("Total Crashes")
    plt.tight_layout()
    plt.savefig("output/charts/yearly_trend.png")
    plt.close()

def plot_single_county(df, county):
    subset = df[df["County"] == county]

    ax = subset.plot(x="Year", y="Crashes")
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))

    plt.title(f"{county} Crash Trend")
    plt.tight_layout()
    plt.savefig(f"output/charts/{county.lower()}_trend.png")
    plt.close()

if __name__ == "__main__":
    df = pd.read_csv("data/cleaned/cleaned_crashes.csv")

    plot_top_counties(df)
    plot_yearly_trend(df)
    plot_single_county(df, "Bergen")
    plot_single_county(df, "Essex")
    plot_single_county(df, "Middlesex")
    plot_single_county(df, "Hudson")
    plot_single_county(df, "Union")

    print("Charts generated.")