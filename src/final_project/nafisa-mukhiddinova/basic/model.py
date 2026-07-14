import pandas as pd
from pathlib import Path
from stats_transformer.models.regression.regression import RegressionModel

def run():
    project_root = Path(__file__).resolve().parents[4]
    data_file = project_root / "data/final_project/nafisa-mukhiddinova/processed_tariff_inflation.csv"
    if not data_file.exists():
        raise FileNotFoundError(f"{data_file} not found. Run manipulate stage first.")

    df = pd.read_csv(data_file)

    # Baseline CPI pass-through model: does lagged tariff-exposed commodity price
    # growth (steel) add predictive power beyond standard PPI/rates/inflation-expectation controls?
    model = RegressionModel(
        target="core_cpi_growth",
        independent_variables=["ppi_growth_lag1", "spread_lag1", "infexp_lag1", "steel_growth_lag1"],
    )
    model.load_data(df)
    model.build_model()

    print("=== Regression Results Summary ===")
    print(model.get_summary())
    return model.get_summary()

if __name__ == "__main__":
    run()
