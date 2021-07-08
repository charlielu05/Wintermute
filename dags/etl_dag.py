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
                "name": "etl-container",
                "command": ["python", "./src/etl.py"],
            },
        ],
    },
    launch_type="FARGATE",
    network_configuration={
        "awsvpcConfiguration": {
            "securityGroups": ["winter-7479"],
            "subnets": ["subnet-0d949ea696200c7b3"],
        },
    },
    tags={
        "Project":"Wintermute"
    },
    awslogs_group="/ecs/wintermute",
    awslogs_stream_prefix="prefix_b/etl-container",  # prefix with container name
)