# Wintermute
Work sample assessment for Zip

# Setup
Terraform Cloud Workspace with name "Wintermute". <br>
AWS Access Key and Secret stored in Terraform Cloud Environment Variables. <br>
Terraform API token stored in Github Secrets as `TF_API_TOKEN`. <br>

# Local Development
Run `make start-dev` <br>
Using Docker extension in VS-Code, attach to the spawned container by right clicking the container `wintermute-dev` and Attach Visual Studio Code.

# Issues
Even though AWS document states that if you leave the `airflow_version` parameter blank it would deploy the latest version, this is not true. If you need Airflow version 2, you need to explicitly add it into the Terraform resource! Otherwise you will need to destroy the infrastructure and re-deploy since AWS MWAA does not support upgrading from version 1 to 2.
