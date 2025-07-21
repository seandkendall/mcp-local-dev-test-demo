import json
import logging
import random

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """
    Lambda function to generate a random number within a specified range.
    
    Expected input format:
    {
        "min": number (optional, default: 0),
        "max": number (optional, default: 100)
    }
    """
    try:
        # Parse the request body
        if 'body' in event:
            body = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
        else:
            body = event
        
        # Get parameters with defaults
        min_val = body.get('min', 0) if body else 0
        max_val = body.get('max', 100) if body else 100
        
        # Validate that inputs are numbers
        if not isinstance(min_val, (int, float)) or not isinstance(max_val, (int, float)):
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'error': "Both 'min' and 'max' must be numbers"
                })
            }
        
        # Validate range
        if min_val > max_val:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'error': f"min value ({min_val}) cannot be greater than max value ({max_val})"
                })
            }
        
        # Generate random number
        result = random.uniform(min_val, max_val)
        
        logger.info(f"Random Number: Generated {result} between {min_val} and {max_val}")
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'operation': 'get_random_number',
                'min': min_val,
                'max': max_val,
                'result': result
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
        logger.error(f"Error in get_random_number: {str(e)}")
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
