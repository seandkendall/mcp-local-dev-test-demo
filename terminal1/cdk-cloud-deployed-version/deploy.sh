#!/bin/bash

# Sean's Tools MCP Server - Cloud Deployment Script
# Supports --profile and --delete flags for AWS deployment

set -e  # Exit on any error

# Default values
PROFILE=""
DELETE_STACK=false
STACK_NAME="CdkCloudDeployedVersionStack"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to show usage
show_usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Deploy Sean's Tools MCP Server to AWS Cloud"
    echo ""
    echo "Options:"
    echo "  --profile PROFILE_NAME    Use specific AWS profile (optional)"
    echo "  --delete                  Delete/destroy the stack instead of deploying"
    echo "  --help                    Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0                        Deploy using default AWS profile"
    echo "  $0 --profile dev          Deploy using 'dev' AWS profile"
    echo "  $0 --delete               Delete the stack using default profile"
    echo "  $0 --profile dev --delete Delete the stack using 'dev' profile"
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --profile)
            PROFILE="$2"
            shift 2
            ;;
        --delete)
            DELETE_STACK=true
            shift
            ;;
        --help)
            show_usage
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            show_usage
            exit 1
            ;;
    esac
done

# Set AWS profile if specified
if [ ! -z "$PROFILE" ]; then
    export AWS_PROFILE="$PROFILE"
    print_info "Using AWS profile: $PROFILE"
fi

# Check if AWS CLI is installed and configured
print_info "Checking AWS CLI configuration..."
if ! command -v aws &> /dev/null; then
    print_error "AWS CLI is not installed. Please install it first:"
    print_error "https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html"
    exit 1
fi

# Test AWS credentials
if ! aws sts get-caller-identity &> /dev/null; then
    print_error "AWS credentials not configured or invalid."
    print_error "Please run 'aws configure' to set up your credentials."
    exit 1
fi

# Get AWS account and region info
AWS_ACCOUNT=$(aws sts get-caller-identity --query Account --output text)
AWS_REGION=$(aws configure get region || echo "us-east-1")
print_info "AWS Account: $AWS_ACCOUNT"
print_info "AWS Region: $AWS_REGION"

# Check if CDK CLI is installed
print_info "Checking CDK CLI..."
if ! command -v cdk &> /dev/null; then
    print_error "CDK CLI is not installed. Please install it first:"
    print_error "npm install -g aws-cdk"
    exit 1
fi

CDK_VERSION=$(cdk --version)
print_info "CDK Version: $CDK_VERSION"

# Handle stack deletion
if [ "$DELETE_STACK" = true ]; then
    print_warning "Deleting stack: $STACK_NAME"
    read -p "Are you sure you want to delete the stack? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_info "Destroying CDK stack..."
        cdk destroy --force
        
        # Restore original MCP configuration
        MCP_CONFIG_PATH="../../terminal2/.amazonq/mcp.json"
        if [ -f "${MCP_CONFIG_PATH}.backup" ]; then
            print_info "Restoring original MCP configuration..."
            mv "${MCP_CONFIG_PATH}.backup" "$MCP_CONFIG_PATH"
            print_success "MCP configuration restored to local-only setup!"
        else
            # Create clean local-only configuration
            cat > "$MCP_CONFIG_PATH" << EOF
{
  "mcpServers": {
    "seans-tools": {
      "command": "python",
      "args": ["../terminal1/seans_tools_mcp_server.py"],
      "env": {}
    }
  }
}
EOF
            print_success "MCP configuration reset to local-only setup!"
        fi
        
        print_success "Stack deleted successfully!"
    else
        print_info "Stack deletion cancelled."
    fi
    exit 0
fi

# Install Python dependencies
print_info "Installing Python dependencies..."
if [ ! -d ".venv" ]; then
    print_info "Creating Python virtual environment..."
    python3 -m venv .venv
fi

source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Check if CDK is bootstrapped
print_info "Checking CDK bootstrap status..."
if ! aws cloudformation describe-stacks --stack-name CDKToolkit &> /dev/null; then
    print_warning "CDK not bootstrapped in this account/region. Bootstrapping now..."
    cdk bootstrap
    print_success "CDK bootstrap completed!"
else
    print_info "CDK already bootstrapped."
fi

# Synthesize the CDK app
print_info "Synthesizing CDK application..."
cdk synth

# Deploy the stack
print_info "Deploying Sean's Tools MCP Server to AWS..."
print_info "This may take a few minutes..."

cdk deploy --require-approval never

# Get the API Gateway URL from stack outputs
print_info "Retrieving API Gateway URL..."
API_URL=$(aws cloudformation describe-stacks \
    --stack-name "$STACK_NAME" \
    --query 'Stacks[0].Outputs[?OutputKey==`APIGatewayURL`].OutputValue' \
    --output text)

if [ ! -z "$API_URL" ]; then
    print_success "Deployment completed successfully!"
    echo ""
    print_info "=== Sean's Tools MCP Server API Endpoints ==="
    echo ""
    print_success "Base URL: $API_URL"
    echo ""
    echo "Math Operations:"
    echo "  POST ${API_URL}math/add"
    echo "  POST ${API_URL}math/subtract"
    echo "  POST ${API_URL}math/multiply"
    echo "  POST ${API_URL}math/divide"
    echo ""
    echo "Random Operations:"
    echo "  POST ${API_URL}random/number"
    echo "  POST ${API_URL}random/list"
    echo "  POST ${API_URL}random/choice"
    echo ""
    print_info "Example usage:"
    echo "curl -X POST ${API_URL}math/add \\"
    echo "  -H 'Content-Type: application/json' \\"
    echo "  -d '{\"a\": 5, \"b\": 3}'"
    echo ""
    print_success "Your Sean's Tools MCP Server is now live in the cloud!"
    echo ""
    print_info "=== MCP Configuration for Cline/Amazon Q Developer Pro ==="
    echo ""
    print_success "Copy and paste this configuration into your mcp.json file:"
    echo ""
    echo "{"
    echo "  \"mcpServers\": {"
    echo "    \"seans-tools-cloud\": {"
    echo "      \"command\": \"npx\","
    echo "      \"args\": ["
    echo "        \"-y\","
    echo "        \"mcp-remote@latest\","
    echo "        \"${API_URL}mcp\""
    echo "      ],"
    echo "      \"env\": {}"
    echo "    }"
    echo "  }"
    echo "}"
    echo ""
    print_info "This uses npx mcp-remote to connect to your cloud MCP server!"
    
    # Update the local mcp.json file automatically
    MCP_CONFIG_PATH="../../terminal2/.amazonq/mcp.json"
    if [ -f "$MCP_CONFIG_PATH" ]; then
        print_info "Updating local MCP configuration..."
        
        # Create backup
        cp "$MCP_CONFIG_PATH" "${MCP_CONFIG_PATH}.backup"
        
        # Update mcp.json with cloud server
        cat > "$MCP_CONFIG_PATH" << EOF
{
  "mcpServers": {
    "seans-tools": {
      "command": "python",
      "args": ["../terminal1/seans_tools_mcp_server.py"],
      "env": {}
    },
    "seans-tools-cloud": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote@latest",
        "${API_URL}mcp"
      ],
      "env": {}
    }
  }
}
EOF
        
        print_success "Local MCP configuration updated!"
        print_info "Backup saved as: ${MCP_CONFIG_PATH}.backup"
    else
        print_warning "Local MCP configuration file not found at: $MCP_CONFIG_PATH"
    fi
    
    print_info "After deployment, restart your MCP client to use both local and cloud tools!"
else
    print_warning "Deployment completed but could not retrieve API URL."
    print_info "Check the AWS CloudFormation console for stack outputs."
fi

print_info "Deployment script completed."
