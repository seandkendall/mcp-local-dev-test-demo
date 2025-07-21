from aws_cdk import (
    Stack,
    Tags,
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
    Duration,
)
from constructs import Construct

class CdkCloudDeployedVersionStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Common tags for all resources
        common_tags = {
            "Project": "SeansToolsMCPServer",
            "Environment": "Production",
            "Owner": "SeanDall",
            "Purpose": "MCP-Tools-Cloud-Deployment"
        }

        # Apply tags to the stack
        for key, value in common_tags.items():
            Tags.of(self).add(key, value)

        # Create Lambda functions for each tool
        
        # Math Operations Lambda Functions
        math_add_function = _lambda.Function(
            self, "MathAddFunction",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="math_add.lambda_handler",
            code=_lambda.Code.from_asset("lambda_functions/math_operations"),
            timeout=Duration.seconds(30),
            memory_size=128,
            description="Add two numbers together"
        )

        math_subtract_function = _lambda.Function(
            self, "MathSubtractFunction",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="math_subtract.lambda_handler",
            code=_lambda.Code.from_asset("lambda_functions/math_operations"),
            timeout=Duration.seconds(30),
            memory_size=128,
            description="Subtract second number from first number"
        )

        math_multiply_function = _lambda.Function(
            self, "MathMultiplyFunction",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="math_multiply.lambda_handler",
            code=_lambda.Code.from_asset("lambda_functions/math_operations"),
            timeout=Duration.seconds(30),
            memory_size=128,
            description="Multiply two numbers together"
        )

        math_divide_function = _lambda.Function(
            self, "MathDivideFunction",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="math_divide.lambda_handler",
            code=_lambda.Code.from_asset("lambda_functions/math_operations"),
            timeout=Duration.seconds(30),
            memory_size=128,
            description="Divide first number by second number"
        )

        # Random Number Generation Lambda Functions
        random_number_function = _lambda.Function(
            self, "RandomNumberFunction",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="get_random_number.lambda_handler",
            code=_lambda.Code.from_asset("lambda_functions/random_operations"),
            timeout=Duration.seconds(30),
            memory_size=128,
            description="Generate a random number within a specified range"
        )

        random_number_list_function = _lambda.Function(
            self, "RandomNumberListFunction",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="get_random_number_list.lambda_handler",
            code=_lambda.Code.from_asset("lambda_functions/random_operations"),
            timeout=Duration.seconds(30),
            memory_size=128,
            description="Generate a list of random numbers"
        )

        random_choice_function = _lambda.Function(
            self, "RandomChoiceFunction",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="get_random_choice.lambda_handler",
            code=_lambda.Code.from_asset("lambda_functions/random_operations"),
            timeout=Duration.seconds(30),
            memory_size=128,
            description="Pick random item(s) from a provided list of choices"
        )

        # MCP Server Lambda Function
        mcp_server_function = _lambda.Function(
            self, "MCPServerFunction",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="mcp_server.lambda_handler",
            code=_lambda.Code.from_asset("lambda_functions/mcp_server"),
            timeout=Duration.seconds(30),
            memory_size=256,
            description="MCP protocol server for all tools"
        )

        # Create API Gateway REST API
        api = apigateway.RestApi(
            self, "SeansToolsAPI",
            rest_api_name="Seans Tools MCP Server API",
            description="REST API for Sean's Tools MCP Server - Math and Random Operations",
            default_cors_preflight_options=apigateway.CorsOptions(
                allow_origins=apigateway.Cors.ALL_ORIGINS,
                allow_methods=apigateway.Cors.ALL_METHODS,
                allow_headers=["Content-Type", "X-Amz-Date", "Authorization", "X-Api-Key"]
            ),
            endpoint_configuration=apigateway.EndpointConfiguration(
                types=[apigateway.EndpointType.REGIONAL]
            )
        )

        # Create resource groups
        math_resource = api.root.add_resource("math")
        random_resource = api.root.add_resource("random")

        # Math operation endpoints
        math_add_resource = math_resource.add_resource("add")
        math_add_resource.add_method(
            "POST",
            apigateway.LambdaIntegration(math_add_function),
            method_responses=[
                apigateway.MethodResponse(
                    status_code="200",
                    response_parameters={
                        "method.response.header.Access-Control-Allow-Origin": True
                    }
                )
            ]
        )

        math_subtract_resource = math_resource.add_resource("subtract")
        math_subtract_resource.add_method(
            "POST",
            apigateway.LambdaIntegration(math_subtract_function)
        )

        math_multiply_resource = math_resource.add_resource("multiply")
        math_multiply_resource.add_method(
            "POST",
            apigateway.LambdaIntegration(math_multiply_function)
        )

        math_divide_resource = math_resource.add_resource("divide")
        math_divide_resource.add_method(
            "POST",
            apigateway.LambdaIntegration(math_divide_function)
        )

        # Random operation endpoints
        random_number_resource = random_resource.add_resource("number")
        random_number_resource.add_method(
            "POST",
            apigateway.LambdaIntegration(random_number_function)
        )

        random_list_resource = random_resource.add_resource("list")
        random_list_resource.add_method(
            "POST",
            apigateway.LambdaIntegration(random_number_list_function)
        )

        random_choice_resource = random_resource.add_resource("choice")
        random_choice_resource.add_method(
            "POST",
            apigateway.LambdaIntegration(random_choice_function)
        )

        # MCP Server endpoint
        mcp_resource = api.root.add_resource("mcp")
        mcp_resource.add_method(
            "POST",
            apigateway.LambdaIntegration(mcp_server_function)
        )

        # Output the API Gateway URL
        from aws_cdk import CfnOutput
        CfnOutput(
            self, "APIGatewayURL",
            value=api.url,
            description="URL of the API Gateway for Sean's Tools MCP Server"
        )

        CfnOutput(
            self, "APIEndpoints",
            value=f"""
Math Operations:
- POST {api.url}math/add
- POST {api.url}math/subtract  
- POST {api.url}math/multiply
- POST {api.url}math/divide

Random Operations:
- POST {api.url}random/number
- POST {api.url}random/list
- POST {api.url}random/choice
            """,
            description="Available API endpoints"
        )
