# Sean's Tools MCP Server - Cloud Deployment

This directory contains the AWS CDK infrastructure code to deploy Sean's Tools MCP Server to the AWS cloud using Lambda functions and API Gateway.

## Architecture

- **Lambda Functions**: Individual functions for each tool operation
- **API Gateway**: REST API to expose the tools via HTTP endpoints
- **CloudWatch Logs**: Centralized logging for all Lambda functions
- **Tagging**: All resources are properly tagged for organization

## Tools Available

### Math Operations
- `POST /math/add` - Add two numbers
- `POST /math/subtract` - Subtract two numbers  
- `POST /math/multiply` - Multiply two numbers
- `POST /math/divide` - Divide two numbers

### Random Operations
- `POST /random/number` - Generate a random number
- `POST /random/list` - Generate a list of random numbers
- `POST /random/choice` - Pick random item(s) from a list

## Prerequisites

Before deploying, ensure you have:

1. **AWS CLI** installed and configured
   ```bash
   aws --version
   aws configure
   ```

2. **CDK CLI** installed
   ```bash
   npm install -g aws-cdk
   cdk --version
   ```

3. **Python 3.11+** installed
   ```bash
   python3 --version
   ```

## Deployment

### Quick Deploy
```bash
./deploy.sh
```

### Deploy with Specific AWS Profile
```bash
./deploy.sh --profile my-aws-profile
```

### Delete/Destroy Stack
```bash
./deploy.sh --delete
```

### Delete with Specific Profile
```bash
./deploy.sh --profile my-aws-profile --delete
```

## Usage Examples

After deployment, you'll receive API endpoints. Here are usage examples:

### Math Operations

**Add two numbers:**
```bash
curl -X POST https://your-api-url/math/add \
  -H 'Content-Type: application/json' \
  -d '{"a": 5, "b": 3}'
```

**Divide numbers:**
```bash
curl -X POST https://your-api-url/math/divide \
  -H 'Content-Type: application/json' \
  -d '{"a": 10, "b": 2}'
```

### Random Operations

**Generate random number:**
```bash
curl -X POST https://your-api-url/random/number \
  -H 'Content-Type: application/json' \
  -d '{"min": 1, "max": 100}'
```

**Generate random number list:**
```bash
curl -X POST https://your-api-url/random/list \
  -H 'Content-Type: application/json' \
  -d '{"count": 5, "min": 1, "max": 10}'
```

**Random choice from list:**
```bash
curl -X POST https://your-api-url/random/choice \
  -H 'Content-Type: application/json' \
  -d '{"choices": ["apple", "banana", "orange"], "count": 2}'
```

## Response Format

All endpoints return JSON responses with this structure:

**Success Response:**
```json
{
  "operation": "add",
  "a": 5,
  "b": 3,
  "result": 8,
  "expression": "5 + 3 = 8"
}
```

**Error Response:**
```json
{
  "error": "Both 'a' and 'b' parameters are required"
}
```

## Resource Tagging

All AWS resources are tagged with:
- `Project`: SeansToolsMCPServer
- `Environment`: Production
- `Owner`: SeanDall
- `Purpose`: MCP-Tools-Cloud-Deployment

## Cost Optimization

- Lambda functions use minimal memory (128MB)
- CloudWatch logs have 1-week retention
- API Gateway is configured for regional endpoints
- All resources support AWS Free Tier usage

## Troubleshooting

### Common Issues

1. **CDK Bootstrap Required**
   ```bash
   cdk bootstrap
   ```

2. **AWS Credentials Not Configured**
   ```bash
   aws configure
   ```

3. **Permission Errors**
   - Ensure your AWS user/role has sufficient permissions for Lambda, API Gateway, and CloudFormation

### Logs and Monitoring

- Lambda function logs: AWS CloudWatch → Log Groups → `/aws/lambda/[function-name]`
- API Gateway logs: AWS CloudWatch → Log Groups → API Gateway execution logs
- Stack events: AWS CloudFormation → Stacks → CdkCloudDeployedVersionStack

## Development

### Project Structure
```
cdk-cloud-deployed-version/
├── app.py                          # CDK app entry point
├── deploy.sh                       # Deployment script
├── requirements.txt                # Python dependencies
├── cdk_cloud_deployed_version/
│   └── cdk_cloud_deployed_version_stack.py  # CDK stack definition
└── lambda_functions/
    ├── math_operations/            # Math Lambda functions
    │   ├── math_add.py
    │   ├── math_subtract.py
    │   ├── math_multiply.py
    │   └── math_divide.py
    └── random_operations/          # Random Lambda functions
        ├── get_random_number.py
        ├── get_random_number_list.py
        └── get_random_choice.py
```

### Local Testing

You can test Lambda functions locally:
```bash
cd lambda_functions/math_operations
python3 -c "
import math_add
event = {'body': '{\"a\": 5, \"b\": 3}'}
result = math_add.lambda_handler(event, None)
print(result)
"
```

## Security

- CORS is enabled for all origins (suitable for development/testing)
- All Lambda functions include input validation
- Error messages don't expose sensitive information
- CloudWatch logs capture all operations for auditing
