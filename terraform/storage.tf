resource "aws_s3_bucket" "wintermute" {
  bucket = "wintermute"
  acl    = "private"

  tags = {
    Name        = "worked-assessment-zip"
    Environment = "Dev"
  }
}