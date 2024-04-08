# EC2 Instance Monitoring Automation

This repository contains CloudFormation and Terraform scripts to automate the provisioning of resources for monitoring newly deployed EC2 instances using AWS Lambda, Amazon SNS, and CloudWatch Events. This setup eliminates the need for manual intervention and enables seamless monitoring of EC2 instances.

## Features

- Automatically provision Lambda function, SNS topic, and CloudWatch Event Rule.
- Monitor newly deployed EC2 instances using CloudWatch Events.
- Integrate with AWS CodeDeploy or Auto Scaling Group for dynamic monitoring.
- Utilize CloudWatch agent metrics for enhanced monitoring capabilities.

## Prerequisites

Before deploying the scripts, ensure that you have the following prerequisites set up:

- AWS account with appropriate permissions to create and manage resources.
- AWS CLI configured with access keys or IAM role.
- Basic knowledge of AWS services like Lambda, SNS, CloudWatch, and EC2.

## Usage

### CloudFormation

The CloudFormation script (`automacticdashboard.yml`) automates the provisioning of resources:

1. Navigate to the AWS CloudFormation console.
2. Click on "Create Stack" and choose "With new resources (standard)".
3. Upload the `automacticdashboard.yml` file.
4. Follow the on-screen instructions, providing necessary parameters like stack name, Lambda function code location, etc.
5. Click "Create Stack" to initiate the provisioning process.
[![Launch Stack](https://raw.githubusercontent.com/vireshsolanki/aws_dashboard_automation/08ac6647f0bef48de29689cbcf70d943b82e427d/automacticdashboard.yaml)](https://console.aws.amazon.com/cloudformation/home#/stacks/new?templateURL=https://raw.githubusercontent.com/vireshsolanki/aws_dashboard_automation/08ac6647f0bef48de29689cbcf70d943b82e427d/automacticdashboard.yaml)




## Resources Provisioned

Both CloudFormation and Terraform scripts provision the following resources:

- Lambda function: Responsible for processing events triggered by CloudWatch Events.
- SNS topic: Used for sending notifications related to EC2 instance events.
- CloudWatch Event Rule: Triggers the Lambda function when EC2 instance state changes occur.

## Monitoring EC2 Instances

Once the resources are provisioned, EC2 instances can be monitored automatically:

1. Any new EC2 instance launches or state changes will trigger the Lambda function.
2. The Lambda function can perform actions like sending notifications via SNS, updating CloudWatch Dashboards, or executing custom logic based on the event.
3. Utilize CloudWatch agent metrics for deeper insights into EC2 instance performance and health.

## Contributing

Contributions to improve and enhance the automation scripts are welcome! Feel free to submit pull requests or open issues for any suggestions or improvements.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
