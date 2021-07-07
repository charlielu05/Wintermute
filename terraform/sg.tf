resource "aws_security_group" "mwaa_sg" {
  name        = "mwaa-sg"
  description = "Security Group for managed airflow"
  vpc_id      = aws_vpc.wintermute_vpc.id

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

}
