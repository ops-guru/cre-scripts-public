#
# CRE AWS Inventory script
# Author: paul@opsguru.io (Paul Podolny)
# Purpose: Scan AWS footprint during CSA or PSA phase

import boto3
import datetime

def get_aws_account_details():
    sts_client = boto3.client('sts')
    identity = sts_client.get_caller_identity()

    account_id = identity['Account']
    account_arn = identity['Arn']
    account_name = account_arn.split('/')[-1]

    iam_client = boto3.client('iam')
    response = iam_client.list_account_aliases()
    account_alias = response['AccountAliases'][0] if response['AccountAliases'] else None

    return account_id, account_name, account_alias

def get_api_gateways(region):
    client = boto3.client('apigateway')
    response = client.get_rest_apis()
    return len(response['items'])

def get_load_balancers(region):
    client = boto3.client('elbv2')
    response = client.describe_load_balancers()
    return len(response['LoadBalancers'])

def get_dynamodb_tables(region):
    dynamodb = boto3.client('dynamodb')
    response = dynamodb.list_tables()
    return len(response['TableNames'])

def get_redshift_clusters(region):
    redshift = boto3.client('redshift')
    response = redshift.describe_clusters()
    return len(response['Clusters'])    

def get_ec2_details(region):
    ec2_client = boto3.client('ec2', region_name=region)

    response = ec2_client.describe_instances()
    reservations = response['Reservations']

    instance_count = 0

    for reservation in reservations:
        instances = reservation['Instances']
        instance_count += len(instances)
        for instance in instances:
            instance_type = instance['InstanceType']
            instance_details = ec2_client.describe_instance_types(InstanceTypes=[instance_type])
    return instance_count

def get_rds_details(region):
    rds_client = boto3.client('rds', region_name=region)

    response = rds_client.describe_db_instances()
    db_instances = response['DBInstances']

    instance_count = len(db_instances)

    for db_instance in db_instances:
        instance_class = db_instance['DBInstanceClass']
        try:
            instance_details = rds_client.describe_orderable_db_instance_options(Engine='any',DBInstanceClass=instance_class)
        except:
            print("couldn't get RDS instance details")

    return instance_count

def get_lambda_details(region):
    lambda_client = boto3.client('lambda', region_name=region)

    response = lambda_client.list_functions()
    functions = response['Functions']

    function_count = len(functions)
    total_concurrency = 0

    for function in functions:
        function_name = function['FunctionName']
        function_details = lambda_client.get_function(FunctionName=function_name)

    return function_count

def get_eks_details(region):
    eks_client = boto3.client('eks', region_name=region)

    response = eks_client.list_clusters()
    clusters = response['clusters']

    cluster_count = len(clusters)

    return cluster_count

def get_ecs_details(region):
    ecs_client = boto3.client('ecs', region_name=region)

    response = ecs_client.list_clusters()
    clusters = response['clusterArns']

    cluster_count = len(clusters)

    return cluster_count

# Main function
if __name__ == '__main__':
    ec2 = boto3.client('ec2')
    account_id, account_name, account_alias = get_aws_account_details()
    regions = [region['RegionName'] for region in ec2.describe_regions()['Regions']]
    time_now = datetime.datetime.now()
    print(f'\nAWS Account ID: {account_id}')
    print(f'AWS Account Alias: {account_alias}')
    print(f'Local time: {time_now}')
    for region in regions:
        print(f"=========================={region}==========================")
        ec2_instances = get_ec2_details(region)
        rds_instances  = get_rds_details(region)
        lambda_functions = get_lambda_details(region)
        eks_clusters = get_eks_details(region)
        ecs_clusters = get_ecs_details(region)
        api_gateways = get_api_gateways(region)
        load_balancers=get_load_balancers(region)
        redshift_clusters = get_redshift_clusters(region)
        dynamodb_tables = get_dynamodb_tables(region)
        print(f'Total number of EC2 instances: {ec2_instances}')
        print(f'Total number of Lambda functions: {lambda_functions}')
        print(f'Total number of RDS instances: {rds_instances}')
        print(f'Total number of API GWs: {api_gateways}')
        print(f'Total number of Load Balancers: {load_balancers}')
        print(f'Total number of EKS clusters: {eks_clusters}')
        print(f'Total number of ECS clusters: {ecs_clusters}')
        print(f'Total number of DynamoDB tables: {dynamodb_tables}')
        print(f'Total number of Redshift clusters: {redshift_clusters}')
        print(f'==========================')
