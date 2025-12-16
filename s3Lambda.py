import json
import boto3
import string
import random

def lambda_handler(event, context):
    print("Received event:")
    print(json.dumps(event, indent=2))

    try:
        agent = event.get('agent')
        action_group = event.get('actionGroup')
        function = event.get('function')
        parameters = event.get('parameters', [])
        session_attributes = event.get('sessionAttributes', {})
        prompt_session_attributes = event.get('promptSessionAttributes', {})

        if not parameters:
            raise Exception("No parameters provided in the request.")

        param_value = parameters[0].get('value')

        if isinstance(param_value, str):
            payload = json.loads(param_value)
        else:
            payload = param_value

        # Generate random 10-character filename
        filename = ''.join(
            random.choices(string.ascii_uppercase + string.digits, k=10)
        ) + ".json"

        # Upload to S3 - BUCKET NAME: databucketsourceside9755
        boto3.client("s3").put_object(
            Bucket="databucketsourceside9755",
            Key=filename,
            Body=json.dumps(payload)
        )

        response_body = {
            'TEXT': {
                'body': f"Upload successful. File name: {filename}"
            }
        }

        final_response = {
            'messageVersion': '1.0',
            'response': {
                'actionGroup': action_group,
                'function': function,
                'functionResponse': {
                    'responseBody': response_body
                }
            },
            'sessionAttributes': session_attributes,
            'promptSessionAttributes': prompt_session_attributes
        }

        return final_response

    except Exception as e:
        return {
            'messageVersion': '1.0',
            'response': {
                'actionGroup': event.get('actionGroup'),
                'function': event.get('function'),
                'functionResponse': {
                    'responseBody': {
                        'TEXT': {
                            'body': f"Upload failed: {str(e)}"
                        }
                    }
                }
            }
        }
