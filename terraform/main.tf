

module "lambda_function" {
  source = "terraform-aws-modules/lambda/aws"

  function_name = "bezos-net-worth-scheduler"
  description   = "Lambda Function to Schedule Daily Jeff Bezos Net Worth tweet."
  handler       = "index.lambda_handler"
  runtime       = "python3.7"
  
  create_package         = false
  local_existing_package = "./package.zip" # Dummy zip to be updated via a Github Action

#   tags = {
#     Name = "bezos scheduler"
#   }
}