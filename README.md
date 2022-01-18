# Update Release Metadata docker action

Update the release metadata JSON for an ECS service.

## Inputs

## `aws-region`

**Required** The AWS region of the service. Default `"us-east-1"`.

## `ecs-cluster`

**Required** The name of the ECS cluster.

## `ecs-service`

**Required** The name of the ECS service.

## `metadata-bucket`

**Required** The name of the metadata bucket.

## `metadata-key`

**Required** The key of the metadata object.

## `release-tag`

**Required** The release tag.

## Example usage

```yaml
uses: tbell83/gh-action-update-ecs-metadata@v0
with:
  aws-region: us-east-1
  ecs-cluster: ecs-cluster-name
  ecs-service: ecs-service-name
  metadata-bucket: s3-bucket-name
  metadata-key: s3-metadata-key
  release-tag: release-tag
```
