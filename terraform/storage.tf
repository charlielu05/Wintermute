resource "aws_s3_bucket" "wintermute" {
  bucket = "wintermute-84"
  acl    = "private"

  versioning {
    enabled = true
  }

  tags = {
    Name        = "worked-assessment-zip"
    Environment = "Dev"
  }
}