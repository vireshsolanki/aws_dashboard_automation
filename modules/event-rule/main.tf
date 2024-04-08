resource "aws_cloudwatch_event_rule" "ec2_state_change_rule" {
  name = "${var.name}-EC2StateChange"
  event_pattern = <<PATTERN
{
  "source": ["aws.ec2"],
  "detail-type": ["EC2 Instance State-change Notification"],
  "detail": {
    "state": ["running"]
  }
}
PATTERN
}

resource "aws_cloudwatch_event_target" "lambda_target" {
    rule = aws_cloudwatch_event_rule.ec2_state_change_rule.name
    target_id = "SendToLambda"
    arn = var.lambda-arn
  
}


resource "aws_lambda_permission" "lambda_invoke_permission" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = var.lambda-name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.ec2_state_change_rule.arn
}
