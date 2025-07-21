import json
import logging

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """
    Lambda function to add two numbers together.
    
    Expected input format:
    {
        "a": number,
        "b": number
    }
    """
    try:
        # Parse the request body
        if 'body' in event:
            body = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
        else:
            body = event
        
        # Validate required parameters
        if 'a' not in body or 'b' not in body:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'error': "Both 'a' and 'b' parameters are required"
                })
            }
        
        a = body['a']
        b = body['b']
        
        # Validate that inputs are numbers
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'error': "Both 'a' and 'b' must be numbers"
                })
            }
        
        # Perform the calculation
        result = a + b
        
        logger.info(f"Math Add: {a} + {b} = {result}")
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'operation': 'add',
                'a': a,
                'b': b,
                'result': result,
                'expression': f"{a} + {b} = {result}"
            })
        }
        
    except json.JSONDecodeError:
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': 'Invalid JSON in request body'
            })
        }
    except Exception as e:
        logger.error(f"Error in math_add: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': 'Internal server error'
            })
        }
