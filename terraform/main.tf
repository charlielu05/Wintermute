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

resource "aws_ecr_repository" "wintermute_ecr" {
  name                 = "wintermute_ecr"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}