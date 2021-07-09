# Wintermute
Work sample assessment for Zip

# Setup
Terraform Cloud Workspace with name "Wintermute". <br>
AWS Access Key and Secret stored in Terraform Cloud Environment Variables. <br>
Terraform API token stored in Github Secrets as 'TF_API_TOKEN'. <br>
Contents of the 'dags' folder needs to be copied into 's3://<s3_directory>/dags/' <br>

# Local Development
Run `make start-dev` <br>
Using Docker extension in VS-Code, attach to the spawned container by right clicking the container `wintermute-dev` and Attach Visual Studio Code.

# Issues
## Terraform Airflow Version
Even though AWS document states that if you leave the `airflow_version` parameter blank it would deploy the latest version, this is not true. If you need Airflow version 2, you need to explicitly add it into the Terraform resource! Otherwise you will need to destroy the infrastructure and re-deploy since AWS MWAA does not support upgrading from version 1 to 2.

## Airflow ECS Operator log group and stream prefix
The variable log group set in the Airflow operator must match with the ECS task definition settings for log group. For stream prefix, you will need to prefix with container name for the Airflow operator `awslogs_stream_prefix` variable. Eg: if ECS task definition `awslogs-stream-prefix` is `ecs` then for the Airflow ECS operator `awslogs_stream_prefix` needs to be named `ecs/<container name>`. <br>
See this blog for more detail (https://www.the-swamp.info/blog/displaying-ecs-fargate-logs-airflow-ui/)
