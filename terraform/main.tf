terraform {
  backend "remote" {
    organization = "cy-data"
    workspaces {
      name = "Wintermute"
    }
  }
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.27"
    }
  }

  required_version = ">= 0.14.9"
}

provider "aws" {
  profile = "default"
  region  = "ap-southeast-2"
}

data "aws_caller_identity" "current" {}

resource "aws_ecr_repository" "wintermute_ecr" {
  name                 = "wintermute_ecr"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

resource "aws_mwaa_environment" "wintermute_airflow_env" {
  dag_s3_path        = "dags/"
  execution_role_arn = aws_iam_role.mwaa_execution_role.arn
  name               = "wintermute"

  network_configuration {
    security_group_ids = [aws_security_group.mwaa_sg.id]
    subnet_ids         = [aws_subnet.private1.id, aws_subnet.private2.id]
  }

  source_bucket_arn = aws_s3_bucket.wintermute.arn
  depends_on = [
    aws_iam_role.mwaa_execution_role,
  ]
}