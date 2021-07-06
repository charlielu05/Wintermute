resource "aws_s3_bucket" "reddit" {
  bucket = "wintermute"
  acl    = "private"

  tags = {
    Name        = "worked-assessment-zip"
    Environment = "Dev"
  }
}