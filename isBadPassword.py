#!/usr/bin/python3

import json
import boto3

print('Loading function')

client = boto3.client('dynamodb')

# Respond
def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }

def lambda_handler(event, context):
    # word = event['pathParameters']['word']

    body = json.loads(event['body'])
    word = body['word']
    print('Looking up if {} is a bad password'.format(word))

    response = client.query(
        TableName='bad-passwords',
        Limit=1,
        KeyConditions={
            'id': {
                'AttributeValueList': [
                    {
                        'S': word
                    }
                ],
                'ComparisonOperator': 'EQ'
            }
        }
    )

    is_bad = response['Count'] > 0

    print(response)
    print('Is {} bad {}'.format(word, is_bad))

    return respond(False, {'response': is_bad})
