variable "aws_region" {
  default = "ap-south-1"
}

variable "name_prefix" {
  description = "Prefix for naming AWS resources"
  type        = string
}

variable "subnet_ids" {
  description = "List of subnet IDs for the EKS cluster"
  type        = list(string)
}
