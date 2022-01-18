#!/usr/local/bin/python
from datetime import datetime
from os import getenv
import json

import boto3

aws_region = getenv("AWS_REGION", "us-east-1")
ecs_cluster = getenv("ECS_CLUSTER", None)
ecs_service = getenv("ECS_SERVICE", None)
metadata_bucket = getenv("METADATA_BUCKET", None)
metadata_key = getenv("METADATA_KEY", None)
release_tag = getenv("RELEASE_TAG", None)

session = boto3.Session(region_name=aws_region)


def make_release():
    return {
        "metadata": {
            "user": "github-action",
            "name": [],
            "tag": release_tag,
            "time": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%SZ"),
            "region": aws_region,
        },
        "tags": get_container_tags(),
    }


def get_metadata():
    metadata = {}
    try:
        s3 = session.resource("s3")
        metadata_obj = s3.Object(metadata_bucket, metadata_key)
        metadata = json.loads(metadata_obj.get()["Body"].read())
    except s3.meta.client.exceptions.NoSuchKey:
        print(f"No such key: {metadata_key}")
        return False

    return metadata


def put_metadata(metadata):
    s3 = session.resource("s3")
    metadata_obj = s3.Object(metadata_bucket, metadata_key)
    return metadata_obj.put(Body=json.dumps(metadata, indent=2))


def get_task_definition():
    return False


def get_container_tags():
    ecs_client = session.client("ecs")
    for service in ecs_client.describe_services(
        cluster=ecs_cluster, services=[ecs_service]
    )["services"]:
        task_def = ecs_client.describe_task_definition(
            taskDefinition=service["taskDefinition"]
        )["taskDefinition"]
        return {
            container_def["image"]
            .split("/")[-1]
            .split(":")[0]: container_def["image"]
            .split("/")[-1]
            .split(":")[1]
            for container_def in task_def["containerDefinitions"]
        }


metadata = get_metadata()
release = make_release()

if metadata:
    if ecs_cluster not in metadata.keys():
        metadata[ecs_cluster] = {ecs_service: [release]}
    elif ecs_service not in metadata[ecs_cluster].keys():
        metadata[ecs_cluster][ecs_service] = [release]
    else:
        metadata[ecs_cluster][ecs_service].append(release)
else:
    metadata = {ecs_cluster: {ecs_service: [release]}}

put_metadata(metadata)
