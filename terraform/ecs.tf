resource "aws_ecs_cluster" "cluster" {
  name               = "wintermute-ecs-cluster"
  capacity_providers = ["FARGATE"]

  default_capacity_provider_strategy {
    capacity_provider = "FARGATE"
    weight            = "100"
  }
}

resource "aws_ecr_repository" "wintermute_ecr" {
  name                 = "wintermute"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

resource "aws_ecs_task_definition" "etl" {
  family = "wintermute-etl-task"
  requires_compatibilities = [
    "FARGATE",
  ]
  task_role_arn      = aws_iam_role.ecs_task_role.arn
  execution_role_arn = aws_iam_role.fargate.arn
  network_mode       = "awsvpc"
  cpu                = 256
  memory             = 512
  container_definitions = jsonencode([
    {
      name       = "wintermute-etl"
      image      = aws_ecr_repository.wintermute_ecr.repository_url
      entryPoint = ["python", "./src/etl.py"]
      logConfiguration = {
        logDriver = "awslogs",
        options = {
          awslogs-group         = "/ecs/fargate_logging",
          awslogs-region        = "ap-southeast-2",
          awslogs-stream-prefix = "ecs",
          awslogs-create-group  = "true"
        }
      }
      essential = true
      portMappings = [
        {
          containerPort = 80
          hostPort      = 80
        }
      ]
    }
  ])
}

resource "aws_ecs_task_definition" "clustering" {
  family = "wintermute-clustering-task"
  requires_compatibilities = [
    "FARGATE",
  ]
  task_role_arn      = aws_iam_role.ecs_task_role.arn
  execution_role_arn = aws_iam_role.fargate.arn
  network_mode       = "awsvpc"
  cpu                = 4096
  memory             = 8192
  container_definitions = jsonencode([
    {
      name       = "wintermute-clustering"
      image      = aws_ecr_repository.wintermute_ecr.repository_url
      entryPoint = ["python", "./src/clustering.py"]
      logConfiguration = {
        logDriver = "awslogs",
        options = {
          awslogs-group         = "/ecs/fargate_logging",
          awslogs-region        = "ap-southeast-2",
          awslogs-stream-prefix = "ecs",
          awslogs-create-group  = "true"
        }
      }
      essential = true
      portMappings = [
        {
          containerPort = 80
          hostPort      = 80
        }
      ]
    }
  ])
}

resource "aws_ecs_task_definition" "report" {
  family = "wintermute-report-task"
  requires_compatibilities = [
    "FARGATE",
  ]
  task_role_arn      = aws_iam_role.ecs_task_role.arn
  execution_role_arn = aws_iam_role.fargate.arn
  network_mode       = "awsvpc"
  cpu                = 4096
  memory             = 8192
  container_definitions = jsonencode([
    {
      name       = "wintermute-report"
      image      = aws_ecr_repository.wintermute_ecr.repository_url
      entryPoint = ["python", "./src/report.py"]
      logConfiguration = {
        logDriver = "awslogs",
        options = {
          awslogs-group         = "/ecs/fargate_logging",
          awslogs-region        = "ap-southeast-2",
          awslogs-stream-prefix = "ecs",
          awslogs-create-group  = "true"
        }
      }
      essential = true
      portMappings = [
        {
          containerPort = 80
          hostPort      = 80
        }
      ]
    }
  ])
}