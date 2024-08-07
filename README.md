# EC2 Instance Monitoring Automation

This repository contains CloudFormation and Terraform scripts to automate the provisioning of resources for monitoring newly deployed EC2 instances using AWS Lambda, Amazon SNS, and CloudWatch Events. This setup eliminates the need for manual intervention and enables seamless monitoring of EC2 instances.

## Features

- Automatically provision Lambda function, SNS topic, and CloudWatch Event Rule.
- Monitor newly deployed EC2 instances using CloudWatch Events.
- Integrate with AWS CodeDeploy or Auto Scaling Group for dynamic monitoring.
- Utilize CloudWatch agent metrics for enhanced monitoring capabilities.
- New CloudFormation and Terraform scripts to update CloudWatch dashboards based on instance health.

## Prerequisites

Before deploying the scripts, ensure that you have the following prerequisites set up:

- AWS account with appropriate permissions to create and manage resources.
- AWS CLI configured with access keys or IAM role.
- Basic knowledge of AWS services like Lambda, SNS, CloudWatch, and EC2.

## Usage

### CloudFormation

The CloudFormation script (`automacticdashboard.yml` and `healthy_instance_automatic_dashboard.yml`) automates the provisioning of resources:

1. **Provision Basic Resources:**
   1. Navigate to the AWS CloudFormation console.
   2. Click on "Create Stack" and choose "With new resources (standard)".
   3. Upload the `automacticdashboard.yml` file.
   4. Follow the on-screen instructions, providing necessary parameters like stack name, Lambda function code location, etc.
   5. Click "Create Stack" to initiate the provisioning process.

2. **Provision Health-Based Dashboard Update:**
   1. Navigate to the AWS CloudFormation console.
   2. Click on "Create Stack" and choose "With new resources (standard)".
   3. Upload the `healthy_instance_automatic_dashboard.yml` file.
   4. Follow the on-screen instructions, providing necessary parameters like stack name, target group ARN, and dashboard name.
   5. Click "Create Stack" to initiate the provisioning process.

### Terraform

The Terraform script (`main.tf`, `variables.tf`, `terraform.tfvars`, and `tgtodashboard.py`) automates the provisioning of resources:

1. **Ensure Terraform is Installed:**
   - Ensure Terraform is installed on your local machine.

2. **Provision Basic Resources:**
   1. Navigate to the directory called `create-dashboard` which contains the Terraform files (`main.tf`, `variables.tf`, `terraform.tfvars`, etc.).
   2. Update the `terraform.tfvars` file with your desired configurations, such as the region, name, email addresses, and dashboard name.
   3. Run `terraform init` to initialize the Terraform configuration.
   4. Run `terraform plan` to preview the resources that will be created.
   5. Run `terraform apply` to apply the configuration and provision the resources.
   6. Confirm the changes by typing `yes` when prompted.

3. **Provision Health-Based Dashboard Update:**
   1. Ensure the `tgtodashboard.zip` file is uploaded to your S3 bucket.
   2. Navigate to the directory with the Terraform files (`tgtodashboard.py`).
   3. Update the `terraform.tfvars` file with your desired configurations.
   4. Run `terraform init` to initialize the Terraform configuration.
   5. Run `terraform plan` to preview the resources that will be created.
   6. Run `terraform apply` to apply the configuration and provision the resources.
   7. Confirm the changes by typing `yes` when prompted.

## Resources Provisioned

Both CloudFormation and Terraform scripts provision the following resources:

- **Lambda Function:** Responsible for processing events triggered by CloudWatch Events and updating dashboards based on instance health.
- **SNS Topic:** Used for sending notifications related to EC2 instance events.
- **CloudWatch Event Rule:** Triggers the Lambda function when EC2 instance state changes occur.
- **CloudWatch Dashboard:** Updated with metrics for healthy instances.

## Monitoring EC2 Instances

Once the resources are provisioned, EC2 instances can be monitored automatically:

1. Any new EC2 instance launches or state changes will trigger the Lambda function.
2. The Lambda function can perform actions like sending notifications via SNS, updating CloudWatch Dashboards, or executing custom logic based on the event.
3. Utilize CloudWatch agent metrics for deeper insights into EC2 instance performance and health.

## Contributing

Contributions to improve and enhance the automation scripts are welcome! Feel free to submit pull requests or open issues for any suggestions or improvements.
