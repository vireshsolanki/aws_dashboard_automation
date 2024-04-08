
resource "aws_iam_policy" "sns_policy" {
  name        = "SNSPolicy"
  description = "Policy for SNS operations"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect   = "Allow",
        Action   = [
          "sns:Publish",
          "sns:Subscribe",
          "sns:Unsubscribe",
          "sns:GetTopicAttributes",
          "sns:SetTopicAttributes",
          "sns:DeleteTopic",
          "sns:ListSubscriptions",
          "sns:ListSubscriptionsByTopic",
          "sns:ListTopics"
        ],
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_policy_attachment" "sns_policy_attachment" {
  name       = "sns-policy-attachment"
  roles      = [var.lambda-role-name]  # Replace with appropriate role
  policy_arn = aws_iam_policy.sns_policy.arn
}

resource "aws_sns_topic" "sns-topic" {
    name = "${var.name}-sns-topic"
  
}


resource "aws_sns_topic_subscription" "sns-topic-subscription" {
    for_each = var.email
    topic_arn = aws_sns_topic.sns-topic.arn
    protocol  = "email"
    endpoint  = each.value
}