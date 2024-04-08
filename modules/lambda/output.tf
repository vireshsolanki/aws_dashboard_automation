output "lambda-role-name"{
    value = aws_iam_role.lambda_execution_role.name
}

output "lambda-name" {
    value = aws_lambda_function.lambda_function.function_name 
}
output "lambda-arn" {
    value = aws_lambda_function.lambda_function.arn
  
}