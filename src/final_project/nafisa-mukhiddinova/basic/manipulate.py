import pandas as pd
from pathlib import Path

def run():
    project_root = Path(__file__).resolve().parents[4]
    data_file = project_root / "data/final_project/nafisa-mukhiddinova/tariff_inflation_monthly.csv"
    if not data_file.exists():
        raise FileNotFoundError(f"{data_file} not found. Run download stage first.")

    df = pd.read_csv(data_file, parse_dates=["date"]).sort_values("date").reset_index(drop=True)

    # Month-over-month growth rates for CPI pass-through and tariff-exposed commodities
    df["core_cpi_growth"] = df["core_cpi_sa"].pct_change() * 100
    df["ppi_growth"] = df["ppi_sa"].pct_change() * 100
    df["steel_growth"] = df["steel_futures"].pct_change() * 100
    df["aluminum_growth"] = df["aluminum_futures"].pct_change() * 100

    # Lag predictors by one month so they are known before the CPI print they forecast
    df["ppi_growth_lag1"] = df["ppi_growth"].shift(1)
    df["steel_growth_lag1"] = df["steel_growth"].shift(1)
    df["aluminum_growth_lag1"] = df["aluminum_growth"].shift(1)
    df["spread_lag1"] = df["spread_10y_2y"].shift(1)
    df["infexp_lag1"] = df["infexp"].shift(1)

    required = ["core_cpi_growth", "ppi_growth_lag1", "spread_lag1", "infexp_lag1", "steel_growth_lag1", "aluminum_growth_lag1"]
    df_clean = df.dropna(subset=required).copy()

    dest_dir = project_root / "data/final_project/nafisa-mukhiddinova"
    dest_file = dest_dir / "processed_tariff_inflation.csv"
    df_clean.to_csv(dest_file, index=False)
    print(f"Data processed and saved to {dest_file.relative_to(project_root)} with shape {df_clean.shape}")
    return df_clean

if __name__ == "__main__":
    run()
