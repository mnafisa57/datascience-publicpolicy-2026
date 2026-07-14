import pandas as pd
from pathlib import Path

def run():
    project_root = Path(__file__).resolve().parents[4]
    source_path = project_root / "data/final_project/nafisa-mukhiddinova/raw/00_MERGED_MONTHLY.csv"
    if not source_path.exists():
        raise FileNotFoundError(f"Source merged panel not found at {source_path}")

    df = pd.read_csv(source_path)
    df = df.drop(columns=[c for c in df.columns if c.startswith("Unnamed")])
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)

    dest_dir = project_root / "data/final_project/nafisa-mukhiddinova"
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_file = dest_dir / "tariff_inflation_monthly.csv"
    df.to_csv(dest_file, index=False)
    print(f"Data acquired and saved to {dest_file.relative_to(project_root)}")
    return df

if __name__ == "__main__":
    run()
