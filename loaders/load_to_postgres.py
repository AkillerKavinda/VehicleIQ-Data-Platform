import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text


load_dotenv()

DB_HOST = os.getenv("POSTGRES_HOST")
DB_PORT = os.getenv("POSTGRES_PORT")
DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")

CSV_PATH = "data/riyasewana_all_listings.csv"
TABLE_NAME = "riyasewana_listings_raw"
SCHEMA_NAME = "bronze"


def main():
    connection_url = (
        f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    engine = create_engine(connection_url)

    df = pd.read_csv(CSV_PATH)

    df["loaded_at"] = pd.Timestamp.now(tz="Asia/Colombo").tz_localize(None) 
    with engine.begin() as connection:
        connection.execute(text("CREATE SCHEMA IF NOT EXISTS bronze;"))

        df.to_sql(
            TABLE_NAME,
            connection,
            schema=SCHEMA_NAME,
            if_exists="replace",
            index=False
        )

    print(f"Loaded {len(df)} rows into bronze.{TABLE_NAME}")


if __name__ == "__main__":
    main()