import json
import logging
import random

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """
    Lambda function to pick random item(s) from a provided list of choices.
    
    Expected input format:
    {
        "choices": array (required),
        "count": integer (optional, default: 1),
        "allow_duplicates": boolean (optional, default: false)
    }
    """
    try:
        # Parse the request body
        if 'body' in event:
            body = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
        else:
            body = event
        
        # Validate required parameter
        if not body or 'choices' not in body:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'error': "'choices' parameter is required"
                })
            }
        
        choices = body['choices']
        count = body.get('count', 1)
        allow_duplicates = body.get('allow_duplicates', False)
        
        # Validate choices
        if not isinstance(choices, list) or len(choices) == 0:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'error': 'choices must be a non-empty array'
                })
            }
        
        # Validate count
        if not isinstance(count, int) or count < 1:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'error': 'count must be a positive integer'
                })
            }
        
        # Check if we can select the requested count without duplicates
        if count > len(choices) and not allow_duplicates:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'error': f"cannot select {count} unique items from {len(choices)} choices. Set allow_duplicates=true or reduce count."
                })
            }
        
        # Make random selection(s)
        if count == 1:
            result = random.choice(choices)
            logger.info(f"Random Choice: Selected '{result}' from {len(choices)} choices")
        else:
            if allow_duplicates:
                result = [random.choice(choices) for _ in range(count)]
            else:
                result = random.sample(choices, count)
            logger.info(f"Random Choice: Selected {count} items from {len(choices)} choices (duplicates: {allow_duplicates})")
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'operation': 'get_random_choice',
                'choices_count': len(choices),
                'count': count,
                'allow_duplicates': allow_duplicates,
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
        logger.error(f"Error in get_random_choice: {str(e)}")
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
