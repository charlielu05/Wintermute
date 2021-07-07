resource "aws_vpc" "wintermute_vpc" {
  cidr_block           = "10.1.0.0/16"
  enable_dns_hostnames = true

  tags = {
    Name = "wintermute_mwaaa_vpc"
  }
}

resource "aws_subnet" "public1" {
  vpc_id     = aws_vpc.wintermute_vpc.id
  cidr_block = var.public_subnet1cidr
}

resource "aws_subnet" "private1" {
  vpc_id     = aws_vpc.wintermute_vpc.id
  cidr_block = var.private_subnet1cidr
}

resource "aws_subnet" "public2" {
  vpc_id     = aws_vpc.wintermute_vpc.id
  cidr_block = var.public_subnet2cidr
}

resource "aws_subnet" "private2" {
  vpc_id     = aws_vpc.wintermute_vpc.id
  cidr_block = var.private_subnet2cidr
}

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.wintermute_vpc.id
  tags = {
    Name = "wintermute_mwaaa_igw"
  }
}

resource "aws_eip" "nat1" {
  vpc = true
}

resource "aws_eip" "nat2" {
  vpc = true
}

resource "aws_nat_gateway" "ngw1" {
  subnet_id     = aws_subnet.public1.id
  allocation_id = aws_eip.nat1.id

  depends_on = [aws_internet_gateway.igw]
}

resource "aws_nat_gateway" "ngw2" {
  subnet_id     = aws_subnet.public2.id
  allocation_id = aws_eip.nat2.id

  depends_on = [aws_internet_gateway.igw]
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.wintermute_vpc.id
}

resource "aws_route_table" "private1" {
  vpc_id = aws_vpc.wintermute_vpc.id
}

resource "aws_route_table" "private2" {
  vpc_id = aws_vpc.wintermute_vpc.id
}

resource "aws_route_table_association" "public_subnet1" {
  subnet_id      = aws_subnet.public1.id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "public_subnet2" {
  subnet_id      = aws_subnet.public2.id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "private_subnet1" {
  subnet_id      = aws_subnet.private1.id
  route_table_id = aws_route_table.private1.id
}

resource "aws_route_table_association" "private_subnet2" {
  subnet_id      = aws_subnet.private2.id
  route_table_id = aws_route_table.private2.id
}

resource "aws_route" "public_igw" {
  route_table_id         = aws_route_table.public.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.igw.id
}

resource "aws_route" "private_ngw1" {
  route_table_id         = aws_route_table.private1.id
  destination_cidr_block = "0.0.0.0/0"
  nat_gateway_id         = aws_nat_gateway.ngw1.id
}

resource "aws_route" "private_ngw2" {
  route_table_id         = aws_route_table.private2.id
  destination_cidr_block = "0.0.0.0/0"
  nat_gateway_id         = aws_nat_gateway.ngw2.id
}

resource "aws_security_group" "no_ingress" {
  name        = "no-ingress-sg"
  description = "Security group with no ingress rule"
  vpc_id      = aws_vpc.wintermute_vpc.id
}

resource "aws_security_group" "http" {
  name        = "http"
  description = "HTTP traffic"
  vpc_id      = aws_vpc.wintermute_vpc.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "TCP"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "https" {
  name        = "https"
  description = "HTTPS traffic"
  vpc_id      = aws_vpc.wintermute_vpc.id

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "TCP"
    cidr_blocks = ["0.0.0.0/0"]
  }
}