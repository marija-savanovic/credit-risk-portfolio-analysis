from pathlib import Path
import sqlite3

import pandas as pd


# ---------------------------------------------------------
# 1. PROJECT PATHS
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATABASE_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "credit_risk.db"
)

SQL_FOLDER = PROJECT_ROOT / "sql"

OUTPUT_FOLDER = (
    PROJECT_ROOT
    / "reports"
    / "sql_results"
)


# ---------------------------------------------------------
# 2. CREATE OUTPUT FOLDER IF IT DOES NOT EXIST
# ---------------------------------------------------------

OUTPUT_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)


# ---------------------------------------------------------
# 3. FUNCTION TO RUN ONE SQL FILE
# ---------------------------------------------------------

def run_query(connection, sql_file):
    """
    Read one SQL file, execute the query,
    and return the result as a pandas DataFrame.
    """

    with open(sql_file, "r", encoding="utf-8") as file:
        query = file.read()

    result = pd.read_sql_query(
        query,
        connection
    )

    return result


# ---------------------------------------------------------
# 4. FUNCTION TO SAVE QUERY RESULT
# ---------------------------------------------------------

def save_result(result, sql_file):
    """
    Save the query result as a CSV file.

    Example:
    01_portfolio_overview.sql
    becomes
    01_portfolio_overview.csv
    """

    output_file = (
        OUTPUT_FOLDER
        / f"{sql_file.stem}.csv"
    )

    result.to_csv(
        output_file,
        index=False
    )

    return output_file


# ---------------------------------------------------------
# 5. MAIN PROGRAM
# ---------------------------------------------------------

def main():

    # Check if database exists
    if not DATABASE_PATH.exists():
        raise FileNotFoundError(
            f"Database not found: {DATABASE_PATH}"
        )

    # Check if SQL folder exists
    if not SQL_FOLDER.exists():
        raise FileNotFoundError(
            f"SQL folder not found: {SQL_FOLDER}"
        )

    # Find all SQL files
    sql_files = sorted(
        SQL_FOLDER.glob("*.sql")
    )

    if not sql_files:
        raise FileNotFoundError(
            f"No SQL files found in: {SQL_FOLDER}"
        )

    print("=" * 80)
    print("CREDIT RISK SQL ANALYSIS")
    print("=" * 80)

    print(f"\nDatabase:")
    print(DATABASE_PATH)

    print(f"\nSQL folder:")
    print(SQL_FOLDER)

    print(f"\nOutput folder:")
    print(OUTPUT_FOLDER)

    print(
        f"\nNumber of SQL files found: "
        f"{len(sql_files)}"
    )

    # Connect to SQLite database
    with sqlite3.connect(DATABASE_PATH) as connection:

        # Run every SQL file
        for sql_file in sql_files:

            print("\n")
            print("=" * 80)
            print(
                f"Running query: {sql_file.name}"
            )
            print("=" * 80)

            try:

                # Run query
                result = run_query(
                    connection,
                    sql_file
                )

                # Print result
                print(
                    result.to_string(
                        index=False
                    )
                )

                # Save result
                output_file = save_result(
                    result,
                    sql_file
                )

                print(
                    f"\nSaved result to:"
                )

                print(output_file)

                print(
                    f"\nRows returned: "
                    f"{len(result)}"
                )

            except Exception as error:

                print(
                    f"\nError while running "
                    f"{sql_file.name}:"
                )

                print(error)

    print("\n")
    print("=" * 80)
    print("SQL ANALYSIS COMPLETE")
    print("=" * 80)


# ---------------------------------------------------------
# 6. RUN PROGRAM
# ---------------------------------------------------------

if __name__ == "__main__":
    main()