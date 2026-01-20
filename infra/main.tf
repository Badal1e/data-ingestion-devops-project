provider "aws" {
  region = "ap-south-1"
}

resource "aws_s3_bucket" "data_bucket" {
  bucket = "badal-data-ingestion-bucket"
}

resource "aws_db_instance" "rds" {
  allocated_storage    = 20
  engine               = "mysql"
  engine_version       = "8.0"
  instance_class       = "db.t3.micro"
  username             = "admin"
  password             = "admin123"
  db_name              = "ingestiondb"
  skip_final_snapshot  = true
  publicly_accessible  = false
}


resource "aws_security_group" "lambda_sg" {
  name = "lambda-sg"
  ingress {
    from_port = 3306
    to_port = 3306
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
