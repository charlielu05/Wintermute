# Wintermute
Work sample assessment for Zip <br>
Dataset consisting of clothing and fashion items containing attributes such as price, brand, gender, descriptions. <br>
Aim is to process the data, fit a unsupervised machine learning model and generate report with insights found. 
- Convert raw JSON data stored in S3 using Python. Result is a CSV file which is stored in S3.
- Using TFIDF to convert the text description into features for K-Means model. Fit K-Means model on the features and save, generated sparse array, sklearn model object and dataframe containing the model cluster assignment into S3.
- Create plot of optimal cluster choice using ELBO method and PCA reduced two dimensional plot. Generate a HTML report using Jinja and Python

All task steps are performed using ECS Fargate orchestrated by AWS Managed Airflow DAG. 
Terraform is used to deploy the entire stack: Managed Airflow, S3, ECR, ECS Cluster & Task defintions, VPC, Subnets, IAM profile and Security groups. <br>

# Setup
Terraform Cloud Workspace with name "Wintermute". <br>
AWS Access Key and Secret stored in Terraform Cloud Environment Variables. <br>
Terraform API token stored in Github Secrets as `TF_API_TOKEN`. <br>
Contents of the 'dags' folder needs to be copied into `s3://<s3_directory>/dags/` <br>
ECS task execution in Airflow requires a valid subnet and security group in the same VPC as managed Airflow. <br>
Currently for each infrastructure destroy and apply, there will be a new subnet and security group generated. <br>
Need to manually change inside the python DAG code `dags/wintermute_dag.py`. <br>
Production implementation would use possibly AWS Parameter Store or similar so these values can be dynamically obtained inside the python code. <br>

# Local Development
Run `make start-dev` <br>
Using Docker extension in VS-Code, attach to the spawned container by right clicking the container `wintermute-dev` and `Attach Visual Studio Code`.

# Issues
## Terraform Airflow Version
Even though AWS document states that if you leave the `airflow_version` parameter blank it would deploy the latest version, this is not true. If you need Airflow version 2, you need to explicitly add it into the Terraform resource! Otherwise you will need to destroy the infrastructure and re-deploy since AWS MWAA does not support upgrading from version 1 to 2.

## Data Quality
Some entries in the column `long_description` information does not match with `brand` and `product_name`. <br>
Dropping `e_material` as column since 31% missing. Filling in color of remaining 6% as `black`. <br>
Filling missing `gender` as `uni-sex`. <br>

## Airflow ECS Operator log group and stream prefix
The variable log group set in the Airflow operator must match with the ECS task definition settings for log group. For stream prefix, you will need to prefix with container name for the Airflow operator `awslogs_stream_prefix` variable. Eg: if ECS task definition `awslogs-stream-prefix` is `ecs` then for the Airflow ECS operator `awslogs_stream_prefix` needs to be named `ecs/<container name>`. <br>
See this blog for more detail (https://www.the-swamp.info/blog/displaying-ecs-fargate-logs-airflow-ui/)

## ECR repository
After infra destroy using Terraform, the Dockerfile inside the ECR container registry needs to be rebuilt. This means the full CI/CD pipeline using Github actions needs to be executed instead of just `terraform apply`.


