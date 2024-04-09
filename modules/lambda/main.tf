resource "aws_iam_role" "lambda_execution_role" {
  name = "${var.name}-Role"

  assume_role_policy = jsonencode({
    Version   = "2012-10-17"
    Statement = [
      {
        Effect    = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
        Action    = "sts:AssumeRole"
      }
    ]
  })

  tags = {
    Name = "${var.name}-Role"
  }
}

resource "aws_iam_policy" "lambda_execution_policy" {
  name   = "${var.name}-Policy"
  policy = jsonencode({
    Version   = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = [
          "cloudwatch:PutDashboard",
          "cloudwatch:GetDashboard",
          "ec2:Describe*",
          "ec2:Get*",
          "ec2:List*",
          "sns:*",
          "cloudwatch:*"

        ]
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_policy_attachment" "lambda_execution_custom_policy_attachment" {
  name       = "${var.name}-Custom-Policy-Attachment"
  roles      = [aws_iam_role.lambda_execution_role.name]
  policy_arn = aws_iam_policy.lambda_execution_policy.arn
}


resource "aws_lambda_function" "lambda_function" {
  function_name = "${var.name}-Lambda"
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.8"
  timeout       = 800
  role          = aws_iam_role.lambda_execution_role.arn

  environment {
    variables = {
      dashboardname = var.dashboardname
      snstopic     = var.sns-topic-arn
          }
  }
  filename         = "D:/Devops project/Automatic_dashboard/modules/lambda/lambdafunction.zip"
}