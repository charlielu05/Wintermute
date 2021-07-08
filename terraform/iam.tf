resource "aws_iam_role" "mwaa_execution_role" {
  name = "mwaa-role"
  path = "/service-role/"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = ""
        Principal = {
          Service = [
            "airflow-env.amazonaws.com",
            "airflow.amazonaws.com"
          ]
        }
      },
    ]
  })
}

resource "aws_iam_role_policy" "mwaa_policy" {
  name = "mwaa-policy"
  role = aws_iam_role.mwaa_execution_role.id

  policy = jsonencode({
    Version : "2012-10-17",
    Statement : [
      {
        Action : "s3:ListAllMyBuckets"
        Effect : "Deny",
        Resource : [aws_s3_bucket.wintermute.arn,
          "${aws_s3_bucket.wintermute.arn}/*",
        ]
      },
      {
        Action : "airflow:PublishMetrics"
        Effect : "Allow",
        Resource : "*"
      },
      {
        Action : ["s3:*"]
        Effect : "Allow",
        Resource : [aws_s3_bucket.wintermute.arn,
          "${aws_s3_bucket.wintermute.arn}/*",
        ]
      },
      {
        Action : "log:DescribeLogGroups"
        Effect : "Allow",
        Resource : "*"
      },
      {
        Action : ["logs:CreateLogStream",
          "logs:CreateLogGroup",
          "logs:PutLogEvents",
          "logs:GetLogEvents",
          "logs:GetLogRecord",
          "logs:GetLogGroupFields",
          "logs:GetQueryResults",
        "logs:DescribeLogGroups"]
        Effect : "Allow",
        Resource : "*"
      },
      {
        Action : "cloudwatch:PutMetricData"
        Effect : "Allow",
        Resource : "*"
      },
      {
        Action : "sqs:*"
        Effect : "Allow",
        Resource : "arn:aws:sqs:ap-southeast-2:*:airflow-celery-*"
      },
      {
        Action : ["kms:Decrypt", "kms:DescribeKey", "kms:GenerateDataKey", "kms:Encrypt"]
        Effect : "Allow",
        Resource : "*"
      },
    ]
  })
}

resource "aws_iam_role" "fargate" {
  name = "fargate-role"
  path = "/serviceaccounts/"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = ""
        Principal = {
          Service = [
            "ecs.amazonaws.com",
            "ecs-tasks.amazonaws.com"
          ]
        }
      },
    ]
  })
}

resource "aws_iam_role_policy" "fargate" {
  name = "fargate-execution-role"
  role = aws_iam_role.fargate.id

  policy = jsonencode({
    Version : "2012-10-17",
    Statement : [
      {
        Action : [
          "ecr:CompleteLayerUpload",
          "ecr:BatchCheckLayerAvailability",
          "ecr:DescribeRepositories",
          "ecr:BatchGetImage",
          "ecr:ListImages",
          "ecr:DescribeImages",
          "ecr:GetAuthorizationToken",
          "ecr:GetDownloadUrlForLayer",
          "ecr:GetLifecyclePolicy",
          "logs:CreateLogStream",
          "logs:PutLogEvents",
          "logs:CreateLogGroup"
        ],
        Effect : "Allow",
        Resource : "*"
      }
    ]
  })
}

resource "aws_iam_role" "ecs_task_role" {
  name = "reddit-scrape-task"

  assume_role_policy = <<EOF
{
 "Version": "2012-10-17",
 "Statement": [
   {
     "Action": "sts:AssumeRole",
     "Principal": {
       "Service": "ecs-tasks.amazonaws.com"
     },
     "Effect": "Allow",
     "Sid": ""
   }
 ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "task_s3" {
  role       = aws_iam_role.ecs_task_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

