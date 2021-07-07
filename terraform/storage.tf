resource "aws_s3_account_public_access_block" "wintermute_s3_block" {
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

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