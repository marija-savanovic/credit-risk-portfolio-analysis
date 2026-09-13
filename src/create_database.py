from pathlib import Path
import sqlite3

import pandas as pd


def main() -> None:
    project_root = Path(__file__).resolve().parent.parent

    input_path = (
        project_root
        / "data"
        / "processed"
        / "credit_risk_clean.csv"
    )

    database_path = (
        project_root
        / "data"
        / "processed"
        / "credit_risk.db"
    )

    if not input_path.exists():
        raise FileNotFoundError(
            f"Cleaned dataset not found: {input_path}"
        )

    data = pd.read_csv(input_path)

    with sqlite3.connect(database_path) as connection:
        data.to_sql(
            "credit_risk",
            connection,
            if_exists="replace",
            index=False
        )

    print(f"Database created at: {database_path}")


if __name__ == "__main__":
    main()