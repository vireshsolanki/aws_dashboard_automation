import json
import boto3
import datetime
import time

MAX_RETRIES = 16   # Number of retries (e.g., 16 retries with 30-second intervals)
RETRY_INTERVAL = 30  # Interval between retries in seconds

def lambda_handler(event, context):
    # Extract instance id from the event
    instance_id = event['detail']['instance-id']
    
    # Check if the instance is healthy in the target group
    if not is_instance_healthy(instance_id):
        print(f"Instance {instance_id} is not healthy. Skipping dashboard update.")
        return {
            'statusCode': 200,
            'body': json.dumps('Instance is not healthy, dashboard update skipped.')
        }
    
    # Calculate the start time and end time
    start_time = datetime.datetime.utcnow() - datetime.timedelta(hours=1)  # Example: 1 hour ago
    end_time = datetime.datetime.utcnow()
    
    # Create a CloudWatch client
    cloudwatch = boto3.client('cloudwatch')
    
    # Get the EC2 instance's CPU utilization metrics
    response_cpu = cloudwatch.get_metric_statistics(
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
    if 'Datapoints' in response_cpu and len(response_cpu['Datapoints']) > 0:
        cpu_utilization = response_cpu['Datapoints'][0]['Average']
    else:
        cpu_utilization = "No data available"

    # Print CPU utilization
    print("CPU Utilization:", cpu_utilization)
    
    # Update the CloudWatch Dashboard and add alarms for CPU Utilization
    update_dashboard(instance_id, cpu_utilization)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Successfully retrieved CPU utilization, updated CloudWatch Dashboard, and added alarms!')
    }

def is_instance_healthy(instance_id):
    elb_client = boto3.client('elbv2')
    target_group_arn = 'testarn'  # Replace with your Target Group ARN
    
    retries = 0
    while retries < MAX_RETRIES:
        response = elb_client.describe_target_health(
            TargetGroupArn=target_group_arn,
            Targets=[{'Id': instance_id}]
        )
        
        for target_health in response['TargetHealthDescriptions']:
            if target_health['Target']['Id'] == instance_id:
                state = target_health['TargetHealth']['State']
                print(f"Instance {instance_id} health check state: {state}")
                if state == 'healthy':
                    return True
                elif state in ['initial', 'unhealthy']:
                    print(f"Instance {instance_id} is not healthy. Retrying...")
        
        retries += 1
        time.sleep(RETRY_INTERVAL)  # Wait before retrying
    
    print(f"Instance {instance_id} did not reach a healthy state after {MAX_RETRIES * RETRY_INTERVAL / 60} minutes.")
    return False

def update_dashboard(instance_id, cpu_utilization):
    # Create a CloudWatch client
    cloudwatch = boto3.client('cloudwatch')
    
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
                    "region": "ap-south-1", #region name
                    "title": "test"
                }
            }
        ]
    }

    # Update the CloudWatch Dashboard
    response = cloudwatch.put_dashboard(
        DashboardName='test', ##Dashboard name
        DashboardBody=json.dumps(dashboard_body)
    )
    
    print("Dashboard update response:", response)

    # Add CloudWatch Alarms for CPU Utilization
    alarm_cpu_75 = cloudwatch.put_metric_alarm(
        AlarmName='CPUUtilizationAlarm75webserverautoscaling',
        ComparisonOperator='GreaterThanOrEqualToThreshold',
        EvaluationPeriods=1,
        MetricName='CPUUtilization',
        Namespace='AWS/EC2',
        Period=300,
        Statistic='Average',
        Threshold=75,
        ActionsEnabled=True,
        AlarmActions=['your alarm arn'],
        Dimensions=[
            {
                'Name': 'InstanceId',
                'Value': instance_id
            },
        ]
    )

    alarm_cpu_100 = cloudwatch.put_metric_alarm(
        AlarmName='CPUUtilizationAlarm100webserverautoscaling',
        ComparisonOperator='GreaterThanOrEqualToThreshold',
        EvaluationPeriods=1,
        MetricName='CPUUtilization',
        Namespace='AWS/EC2',
        Period=300,
        Statistic='Average',
        Threshold=100,
        ActionsEnabled=True,
        AlarmActions=['your alarm arn'],
        Dimensions=[
            {
                'Name': 'InstanceId',
                'Value': instance_id
            },
        ]
    )
    
    print("Alarms created for CPU Utilization (75% and 100%).")
