variable "public_subnet1cidr" {
  description = "CIDR range of public subnet 1"
  type        = string
  default     = "10.192.10.0/24"
}

variable "private_subnet1cidr" {
  description = "CIDR range of private subnet 1"
  type        = string
  default     = "10.192.20.0/24"
}

variable "public_subnet2cidr" {
  description = "CIDR range of public subnet 2"
  type        = string
  default     = "10.192.11.0/24"
}

variable "private_subnet2cidr" {
  description = "CIDR range of private subnet 2"
  type        = string
  default     = "10.192.21.0/24"
}

variable "subnet_az1" {
  description = "AZ for subnet 1"
  type        = string
  default     = "ap-southeast-2a"
}

variable "subnet_az2" {
  description = "AZ for subnet 2"
  type        = string
  default     = "ap-southeast-2b"
}

variable "max_worker_nodes" {
  description = "Maximum number of workers that can run in the environment"
  type        = number
  default     = 2
}