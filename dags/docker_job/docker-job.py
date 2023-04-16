from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.docker_operator import DockerOperator
from airflow.operators.dummy_operator import DummyOperator

default_args = {
    "owner": "airflow",
    "description": "Use of the DockerOperator",
    "depend_on_past": False,
    "start_date": datetime(2023, 3, 1),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    "estimate_pi_dag",
    default_args=default_args,
    schedule_interval="@daily",
    catchup=False,
) as dag:
    start_dag = DummyOperator(task_id="start_dag")

    spark_job = DockerOperator(
        task_id="docker-estimate-pi",
        image="pi-estimate-task",
        container_name="task___estimate-pi",
        api_version="auto",
        auto_remove=True,
        command="spark-submit ./pi-estimate.py",
        docker_url="tcp://docker-proxy:2375",
        mount_tmp_dir=False,
        environment={"NUM_SAMPLES": 1000},
        network_mode="default_network",  # run the docker container in the same network as localstack
    )

    end_dag = DummyOperator(task_id="end_dag")

    start_dag >> spark_job >> end_dag
