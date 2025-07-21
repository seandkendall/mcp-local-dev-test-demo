import json
import random
import logging
from typing import Any, Dict, List

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """
    Lambda function that implements MCP protocol over HTTP.
    This handles MCP requests and returns MCP-formatted responses.
    """
    try:
        # Handle OPTIONS requests for CORS
        if event.get('httpMethod') == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'POST, OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type, Authorization'
                },
                'body': ''
            }
        
        # Parse the request
        if 'body' in event:
            body = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
        else:
            body = event
        
        # Handle MCP protocol messages
        if 'method' in body:
            method = body['method']
            params = body.get('params', {})
            request_id = body.get('id')
            
            if method == 'initialize':
                # Handle MCP initialization
                protocol_version = params.get('protocolVersion', '2024-11-05')
                client_info = params.get('clientInfo', {})
                
                result = {
                    'protocolVersion': '2024-11-05',
                    'capabilities': {
                        'tools': {}
                    },
                    'serverInfo': {
                        'name': 'seans-tools-cloud',
                        'version': '1.0.0'
                    }
                }
                return create_mcp_response(request_id, result)
            elif method == 'initialized':
                # Handle initialized notification (no response needed)
                return {
                    'statusCode': 200,
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': 'POST, OPTIONS',
                        'Access-Control-Allow-Headers': 'Content-Type, Authorization'
                    },
                    'body': ''
                }
            elif method == 'tools/list':
                return create_mcp_response(request_id, list_tools())
            elif method == 'tools/call':
                tool_name = params.get('name')
                arguments = params.get('arguments', {})
                result = call_tool(tool_name, arguments)
                return create_mcp_response(request_id, result)
            else:
                return create_mcp_error(request_id, -32601, f"Method not found: {method}")
        else:
            return create_mcp_error(None, -32600, "Invalid Request")
            
    except json.JSONDecodeError:
        return create_mcp_error(None, -32700, "Parse error")
    except Exception as e:
        logger.error(f"Error in MCP server: {str(e)}")
        return create_mcp_error(None, -32603, f"Internal error: {str(e)}")

def create_mcp_response(request_id, result):
    """Create a properly formatted MCP response."""
    response = {
        'jsonrpc': '2.0',
        'id': request_id,
        'result': result
    }
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization'
        },
        'body': json.dumps(response)
    }

def create_mcp_error(request_id, code, message):
    """Create a properly formatted MCP error response."""
    response = {
        'jsonrpc': '2.0',
        'id': request_id,
        'error': {
            'code': code,
            'message': message
        }
    }
    
    return {
        'statusCode': 200,  # MCP errors are still HTTP 200
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization'
        },
        'body': json.dumps(response)
    }

def list_tools():
    """Return the list of available tools in MCP format."""
    return {
        'tools': [
            {
                'name': 'get_random_number',
                'description': 'Generate a random number within a specified range',
                'inputSchema': {
                    'type': 'object',
                    'properties': {
                        'min': {'type': 'number', 'description': 'Minimum value (default: 0)', 'default': 0},
                        'max': {'type': 'number', 'description': 'Maximum value (default: 100)', 'default': 100}
                    },
                    'additionalProperties': False
                }
            },
            {
                'name': 'get_random_number_list',
                'description': 'Generate a list of random numbers',
                'inputSchema': {
                    'type': 'object',
                    'properties': {
                        'count': {'type': 'integer', 'description': 'Number of random numbers to generate (default: 5)', 'default': 5, 'minimum': 1, 'maximum': 1000},
                        'min': {'type': 'number', 'description': 'Minimum value for each number (default: 0)', 'default': 0},
                        'max': {'type': 'number', 'description': 'Maximum value for each number (default: 100)', 'default': 100}
                    },
                    'additionalProperties': False
                }
            },
            {
                'name': 'get_random_choice',
                'description': 'Pick random item(s) from a provided list of choices',
                'inputSchema': {
                    'type': 'object',
                    'properties': {
                        'choices': {'type': 'array', 'description': 'List of items to choose from', 'items': {'type': ['string', 'number', 'boolean']}, 'minItems': 1},
                        'count': {'type': 'integer', 'description': 'Number of items to select (default: 1)', 'default': 1, 'minimum': 1},
                        'allow_duplicates': {'type': 'boolean', 'description': 'Allow selecting the same item multiple times (default: false)', 'default': False}
                    },
                    'required': ['choices'],
                    'additionalProperties': False
                }
            },
            {
                'name': 'math_add',
                'description': 'Add two numbers together',
                'inputSchema': {
                    'type': 'object',
                    'properties': {
                        'a': {'type': 'number', 'description': 'First number'},
                        'b': {'type': 'number', 'description': 'Second number'}
                    },
                    'required': ['a', 'b'],
                    'additionalProperties': False
                }
            },
            {
                'name': 'math_subtract',
                'description': 'Subtract second number from first number',
                'inputSchema': {
                    'type': 'object',
                    'properties': {
                        'a': {'type': 'number', 'description': 'First number (minuend)'},
                        'b': {'type': 'number', 'description': 'Second number (subtrahend)'}
                    },
                    'required': ['a', 'b'],
                    'additionalProperties': False
                }
            },
            {
                'name': 'math_multiply',
                'description': 'Multiply two numbers together',
                'inputSchema': {
                    'type': 'object',
                    'properties': {
                        'a': {'type': 'number', 'description': 'First number'},
                        'b': {'type': 'number', 'description': 'Second number'}
                    },
                    'required': ['a', 'b'],
                    'additionalProperties': False
                }
            },
            {
                'name': 'math_divide',
                'description': 'Divide first number by second number',
                'inputSchema': {
                    'type': 'object',
                    'properties': {
                        'a': {'type': 'number', 'description': 'Dividend (number to be divided)'},
                        'b': {'type': 'number', 'description': 'Divisor (number to divide by)'}
                    },
                    'required': ['a', 'b'],
                    'additionalProperties': False
                }
            }
        ]
    }

def call_tool(name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Execute a tool and return the result in MCP format."""
    
    if name == "get_random_number":
        min_val = arguments.get("min", 0)
        max_val = arguments.get("max", 100)
        
        if min_val > max_val:
            raise ValueError(f"min value ({min_val}) cannot be greater than max value ({max_val})")
        
        result = random.uniform(min_val, max_val)
        return {
            'content': [{'type': 'text', 'text': f"Random number: {result}"}]
        }
    
    elif name == "get_random_number_list":
        count = arguments.get("count", 5)
        min_val = arguments.get("min", 0)
        max_val = arguments.get("max", 100)
        
        if min_val > max_val:
            raise ValueError(f"min value ({min_val}) cannot be greater than max value ({max_val})")
        
        if count < 1 or count > 1000:
            raise ValueError(f"count must be between 1 and 1000, got {count}")
        
        numbers = [random.uniform(min_val, max_val) for _ in range(count)]
        return {
            'content': [{'type': 'text', 'text': f"Random numbers: {numbers}"}]
        }
    
    elif name == "get_random_choice":
        choices = arguments.get("choices")
        count = arguments.get("count", 1)
        allow_duplicates = arguments.get("allow_duplicates", False)
        
        if not choices:
            raise ValueError("choices parameter is required and cannot be empty")
        
        if count > len(choices) and not allow_duplicates:
            raise ValueError(f"cannot select {count} unique items from {len(choices)} choices. Set allow_duplicates=true or reduce count.")
        
        if count == 1:
            result = random.choice(choices)
            return {
                'content': [{'type': 'text', 'text': f"Random choice: {result}"}]
            }
        else:
            if allow_duplicates:
                result = [random.choice(choices) for _ in range(count)]
            else:
                result = random.sample(choices, count)
            return {
                'content': [{'type': 'text', 'text': f"Random choices: {result}"}]
            }
    
    elif name == "math_add":
        a = arguments.get("a")
        b = arguments.get("b")
        
        if a is None or b is None:
            raise ValueError("Both 'a' and 'b' parameters are required")
        
        result = a + b
        return {
            'content': [{'type': 'text', 'text': f"{a} + {b} = {result}"}]
        }
    
    elif name == "math_subtract":
        a = arguments.get("a")
        b = arguments.get("b")
        
        if a is None or b is None:
            raise ValueError("Both 'a' and 'b' parameters are required")
        
        result = a - b
        return {
            'content': [{'type': 'text', 'text': f"{a} - {b} = {result}"}]
        }
    
    elif name == "math_multiply":
        a = arguments.get("a")
        b = arguments.get("b")
        
        if a is None or b is None:
            raise ValueError("Both 'a' and 'b' parameters are required")
        
        result = a * b
        return {
            'content': [{'type': 'text', 'text': f"{a} × {b} = {result}"}]
        }
    
    elif name == "math_divide":
        a = arguments.get("a")
        b = arguments.get("b")
        
        if a is None or b is None:
            raise ValueError("Both 'a' and 'b' parameters are required")
        
        if b == 0:
            raise ValueError("Division by zero is not allowed")
        
        result = a / b
        return {
            'content': [{'type': 'text', 'text': f"{a} ÷ {b} = {result}"}]
        }
    
    else:
        raise ValueError(f"Unknown tool: {name}")
