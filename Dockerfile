FROM apache/airflow:2.10.5

RUN pip install --no-cache-dir \
    pandas \
    sqlalchemy \
    psycopg2-binary \
    python-dotenv \
    dbt-postgres