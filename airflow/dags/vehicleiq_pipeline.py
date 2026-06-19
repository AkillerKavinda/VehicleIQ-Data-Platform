from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

PROJECT_DIR = "/opt/airflow/project"
DBT_DIR = "/opt/airflow/project/dbt_vehicleiq"
DBT_PROFILES_DIR = "/opt/airflow/project/dbt_vehicleiq/.dbt"

with DAG(
    dag_id="vehicleiq_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
) as dag:

    load_to_bronze = BashOperator(
        task_id="load_to_bronze",
        bash_command=f"""
        cd {PROJECT_DIR} &&
        python loaders/load_to_postgres.py
        """,
    )

    run_dbt_models = BashOperator(
        task_id="run_dbt_models",
        bash_command=f"""
        cd {DBT_DIR} &&
        /home/airflow/.local/bin/dbt run --profiles-dir {DBT_PROFILES_DIR}
        """,
    )

    run_dbt_tests = BashOperator(
        task_id="run_dbt_tests",
        bash_command=f"""
        cd {DBT_DIR} &&
        /home/airflow/.local/bin/dbt test --profiles-dir {DBT_PROFILES_DIR}
        """,
    )

    load_to_bronze >> run_dbt_models >> run_dbt_tests