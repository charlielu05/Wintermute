import datetime
import os

from airflow import DAG
from airflow.providers.amazon.aws.operators.ecs import ECSOperator

DEFAULT_ARGS = {
    "owner": "airflow",
    "depends_on_past": False,
    "email": ["airflow@example.com"],
    "email_on_failure": False,
    "email_on_retry": False,
}

dag = DAG(
    dag_id="ecs_fargate_dag",
    default_args=DEFAULT_ARGS,
    default_view="graph",
    schedule_interval=None,
    start_date=datetime.datetime(2020, 1, 1),
    tags=["example"],
)
# generate dag documentation
dag.doc_md = __doc__

# [START howto_operator_ecs]
hello_world = ECSOperator(
    task_id="wintermute_etl",
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
            "securityGroups": ["sg-071e5526f26f4e5af"],
            "subnets": ["subnet-0506ef589257e792a"],
        },
    },
    tags={
        "Project":"Wintermute"
    },
    awslogs_group="/ecs/fargate_logging",
    awslogs_stream_prefix="ecs/wintermute-etl",  # prefix with container name
)