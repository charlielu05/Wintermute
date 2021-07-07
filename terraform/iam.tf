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
        Action : ["s3:GetObject*", "s3:GetBucket*", "s3:List*"]
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
        Action : ["kms:Decrypt", "kms:DescribeKey", "kms:GenerateDataKey*", "kms:Encrypt"]
        Effect : "Allow",
        NotResource : "arn:aws:kms:*:${data.aws_caller_identity.current.account_id}:key/*"
        condition : {
          test     = "StringLike"
          variable = "kms:ViaService"
          values   = "sqs.ap-southeast-2.amazonaws.com"
        }
      },
    ]
  })
}