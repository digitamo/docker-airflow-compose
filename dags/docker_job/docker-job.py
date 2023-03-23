from datetime import datetime, timedelta

from airflow import DAG
from airflow.models import Connection
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.operators.bash_operator import BashOperator
from airflow.operators.docker_operator import DockerOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor


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
    "events_ETL_dag",
    default_args=default_args,
    schedule_interval="@daily",
    catchup=False,
) as dag:
    s3_events_key = "s3://user-events/year={{execution_date.strftime('%Y')}}/month={{execution_date.strftime('%m')}}/day={{execution_date.strftime('%d')}}/*"
    s3_sensor = S3KeySensor(
        task_id="check-user-events",
        poke_interval=60,
        timeout=180,
        soft_fail=False,
        retries=2,
        bucket_key=s3_events_key,
        wildcard_match=True,
        aws_conn_id="aws_default",
        dag=dag,
    )

    spark_job = DockerOperator(
        task_id="docker_command_hello",
        image="event-transformation-task",
        container_name="task___command_hello",
        api_version="auto",
        auto_remove=True,
        command="spark-submit ./aggregate-events.py",
        docker_url="tcp://docker-proxy:2375",
        mount_tmp_dir=False,
        environment={"EVENTS_S3_KEY": s3_events_key},
        network_mode="default_network",  # run the docker container in the same network as localstack
    )

    end_dag = DummyOperator(task_id="end_dag")

    s3_sensor >> spark_job >> end_dag
