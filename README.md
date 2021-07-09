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

## Data Quality
Some entries in the column `long_description` information does not match with `brand` and `product_name`. <br>
Missing data: <br>
`df.isna().sum().apply(lambda x: x/df.shape[0])`
brand                                    0.000074
gender                                   0.004731
product_name                             0.000000
e_matched_tokens_categories_formatted    0.000000
e_material                               0.315689
e_color                                  0.062393
<br>
Dropping `e_material` as column since 31% missing. Filling in color of remaining 6% as `black`.
Filling missing `gender` as `uni-sex`.

## Airflow ECS Operator log group and stream prefix
The variable log group set in the Airflow operator must match with the ECS task definition settings for log group. For stream prefix, you will need to prefix with container name for the Airflow operator `awslogs_stream_prefix` variable. Eg: if ECS task definition `awslogs-stream-prefix` is `ecs` then for the Airflow ECS operator `awslogs_stream_prefix` needs to be named `ecs/<container name>`.
