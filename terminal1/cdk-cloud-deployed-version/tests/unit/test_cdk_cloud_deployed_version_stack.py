import aws_cdk as core
import aws_cdk.assertions as assertions

from cdk_cloud_deployed_version.cdk_cloud_deployed_version_stack import CdkCloudDeployedVersionStack

# example tests. To run these tests, uncomment this file along with the example
# resource in cdk_cloud_deployed_version/cdk_cloud_deployed_version_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CdkCloudDeployedVersionStack(app, "cdk-cloud-deployed-version")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
