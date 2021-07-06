resource "aws_s3_bucket" "wintermute" {
  bucket = "wintermute-84"
  acl    = "private"

  tags = {
    Name        = "worked-assessment-zip"
    Environment = "Dev"
  }
}