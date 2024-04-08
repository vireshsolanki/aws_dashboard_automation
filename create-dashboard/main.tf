module "sns-topic" {
    source = "../modules/sns"
    name = var.name
    email = var.email
    lambda-role-name = module.lambda-function.lambda-role-name
}

module "lambda-function" {
    source = "../modules/lambda"
    name = var.name
    sns-topic-arn = module.sns-topic.sns-topic-arn
    dashboardname= var.dashboardname
  
}
module "event-rule" {
    source = "../modules/event-rule"
    name = var.name
    lambda-name = module.lambda-function.lambda-name
    lambda-arn = module.lambda-function.lambda-arn
  
}