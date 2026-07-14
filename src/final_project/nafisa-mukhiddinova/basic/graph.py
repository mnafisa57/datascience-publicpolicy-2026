import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from pathlib import Path

def plot_cpi_vs_commodities(df_full):
    df = df_full.set_index("date")[["core_cpi_sa", "steel_futures", "aluminum_futures"]].copy()
    df_norm = df / df.iloc[0] * 100

    fig, ax = plt.subplots(figsize=(11, 6))
    ax.plot(df_norm.index, df_norm["core_cpi_sa"], color="#1b9e77", linewidth=2.2, label="Core CPI (SA)")
    ax.plot(df_norm.index, df_norm["steel_futures"], color="#d95f02", linewidth=1.6, label="Steel futures")
    ax.plot(df_norm.index, df_norm["aluminum_futures"], color="#7570b3", linewidth=1.6, label="Aluminum futures")

    ax.set_title("Core CPI vs. Tariff-Exposed Metal Futures (Indexed to 100 at Jan 2015)")
    ax.set_xlabel("Date")
    ax.set_ylabel("Index (Jan 2015 = 100)")
    ax.legend(frameon=False)
    ax.grid(alpha=0.25)
    plt.tight_layout()
    plt.show()
    return fig

def plot_ppi_vs_cpi_growth(df_clean):
    fig = plt.figure(figsize=(9, 6))
    sns.scatterplot(data=df_clean, x="ppi_growth_lag1", y="core_cpi_growth", alpha=0.6, color="#1b9e77")
    sns.regplot(data=df_clean, x="ppi_growth_lag1", y="core_cpi_growth", scatter=False, line_kws={"color": "red", "linewidth": 2})

    plt.title("Lagged PPI Growth vs. Core CPI Growth (Monthly)")
    plt.xlabel("PPI Growth, Lagged 1 Month (%)")
    plt.ylabel("Core CPI Growth (%)")
    plt.tight_layout()
    plt.show()
    return fig

def run():
    project_root = Path(__file__).resolve().parents[4]
    full_file = project_root / "data/final_project/nafisa-mukhiddinova/tariff_inflation_monthly.csv"
    clean_file = project_root / "data/final_project/nafisa-mukhiddinova/processed_tariff_inflation.csv"
    if not full_file.exists() or not clean_file.exists():
        raise FileNotFoundError("Processed data not found. Run download and manipulate stages first.")

    df_full = pd.read_csv(full_file, parse_dates=["date"])
    df_clean = pd.read_csv(clean_file, parse_dates=["date"])

    fig1 = plot_cpi_vs_commodities(df_full)
    fig2 = plot_ppi_vs_cpi_growth(df_clean)
    return fig1, fig2

if __name__ == "__main__":
    run()
