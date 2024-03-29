import datetime
import os

from airflow import DAG
from airflow.providers.amazon.aws.operators.ecs import ECSOperator

DEFAULT_ARGS = {
    "owner": "airflow",
    "depends_on_past": False,
    "email": ["charlielu05@gmail.com"],
    "email_on_failure": False,
    "email_on_retry": False,
}

dag = DAG(
    dag_id="wintermute_dag",
    default_args=DEFAULT_ARGS,
    default_view="graph",
    schedule_interval=None,
    start_date=datetime.datetime(2020, 1, 1),
    tags=["wintermute"],
)

# generate dag documentation
dag.doc_md = __doc__

with dag:
    # run ETL task
    etl_task = ECSOperator(
        task_id="etl",
        dag=dag,
        aws_conn_id="aws_ecs",
        cluster="wintermute-ecs-cluster",
        task_definition="wintermute-etl-task",
        overrides={
            "containerOverrides": [
                {
                    "name": "wintermute-etl",
                    "command": ["python", "./src/etl.py"],
                },
            ],
        },
        launch_type="FARGATE",
        network_configuration={
            "awsvpcConfiguration": {
                "securityGroups": ["sg-09371bde9392e7b01"],
                "subnets": ["subnet-05edc2a777bc30ec8"],
            },
        },
        tags={
            "Project":"Wintermute"
        },
        awslogs_group="/ecs/fargate_logging",
        awslogs_stream_prefix="ecs/wintermute-etl",  
    )

    # run clustering task
    cluster_task = ECSOperator(
        task_id="clustering",
        dag=dag,
        aws_conn_id="aws_ecs",
        cluster="wintermute-ecs-cluster",
        task_definition="wintermute-clustering-task",
        overrides={
            "containerOverrides": [
                {
                    "name": "wintermute-clustering",
                    "command": ["python", "./src/clustering.py"],
                },
            ],
        },
        launch_type="FARGATE",
        network_configuration={
            "awsvpcConfiguration": {
                "securityGroups": ["sg-09371bde9392e7b01"],
                "subnets": ["subnet-05edc2a777bc30ec8"],
            },
        },
        tags={
            "Project":"Wintermute"
        },
        awslogs_group="/ecs/fargate_logging",
        awslogs_stream_prefix="ecs/wintermute-clustering",  
    )

    # run report task
    report_task = ECSOperator(
        task_id="report",
        dag=dag,
        aws_conn_id="aws_ecs",
        cluster="wintermute-ecs-cluster",
        task_definition="wintermute-report-task",
        overrides={
            "containerOverrides": [
                {
                    "name": "wintermute-report",
                    "command": ["python", "./src/report.py"],
                },
            ],
        },
        launch_type="FARGATE",
        network_configuration={
            "awsvpcConfiguration": {
                "securityGroups": ["sg-09371bde9392e7b01"],
                "subnets": ["subnet-05edc2a777bc30ec8"],
            },
        },
        tags={
            "Project":"Wintermute"
        },
        awslogs_group="/ecs/fargate_logging",
        awslogs_stream_prefix="ecs/wintermute-report",  
    )

    etl_task >> cluster_task >> report_task
