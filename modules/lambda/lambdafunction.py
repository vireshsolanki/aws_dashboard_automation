import json
import boto3
import datetime

def lambda_handler(event, context):
    # Extract instance id from the event
    instance_id = event['detail']['instance-id']
    # Calculate the start time and end time
    start_time = datetime.datetime.utcnow() - datetime.timedelta(hours=1)  # Example: 1 hour ago
    end_time = datetime.datetime.utcnow()

    # Create a CloudWatch client
    cloudwatch = boto3.client('cloudwatch')

    # Get the EC2 instance's CPU utilization metrics
    response = cloudwatch.get_metric_statistics(
        Namespace='AWS/EC2',
        MetricName='CPUUtilization',
        Dimensions=[
            {
                'Name': 'InstanceId',
                'Value': instance_id
            },
        ],
        StartTime=start_time,
        EndTime=end_time,
        Period=300,
        Statistics=['Average'],
        Unit='Percent'
    )

    # Extracting the average CPU utilization value
    if 'Datapoints' in response and len(response['Datapoints']) > 0:
        cpu_utilization = response['Datapoints'][0]['Average']
    else:
        cpu_utilization = "No data available"

    # Print CPU utilization
    print("CPU Utilization:", cpu_utilization)

    # Update the CloudWatch Dashboard
    update_dashboard(instance_id, cpu_utilization)

    return {
        'statusCode': 200,
        'body': json.dumps('Successfully retrieved CPU utilization and updated CloudWatch Dashboard!')
    }

def update_dashboard(instance_id, cpu_utilization):
    # Define the JSON layout of the dashboard
    dashboard_body = {
        "widgets": [
            {
                "type": "metric",
                "x": 0,
                "y": 0,
                "width": 12,
                "height": 6,
                "properties": {
                    "metrics": [
                        ["AWS/EC2", "CPUUtilization", "InstanceId", instance_id]
                    ],
                    "period": 300,
                    "stat": "Average",
                    "region": "ap-south-1",
                    "title": "EC2 Instance CPU Utilization"
                }
            }
        ]
    }

    # Create a CloudWatch client
    cloudwatch = boto3.client('cloudwatch')

    # Update the CloudWatch Dashboard
    response = cloudwatch.put_dashboard(
        DashboardName="${dashboardname}",  # Replace "YourDashboardName" with your desired name
        DashboardBody=json.dumps(dashboard_body)
    )

    print("Dashboard update response:", response)

    # Add CloudWatch Alarms
    alarm_cpu = cloudwatch.put_metric_alarm(
        AlarmName='CPUUtilizationAlarm',
        ComparisonOperator='GreaterThanOrEqualToThreshold',
        EvaluationPeriods=1,
        MetricName='CPUUtilization',
        Namespace='AWS/EC2',
        Period=300,
        Statistic='Average',
        Threshold=75,
        ActionsEnabled=True,
        AlarmActions=["${snstopic}"],
        Dimensions=[
            {
                'Name': 'InstanceId',
                'Value': instance_id
            }
        ]
    )
