#!/usr/bin/python3

import json
import boto3
import re

print('Loading function')

client = boto3.client('dynamodb')
special_chars = "!@#$%^&*?<>"

# Respond
def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }

def is_valid_password(password):
    if (len(password) < 8
        or not re.search("[A-Z]{1,}", password)
        or not re.search("[a-z]{1,}", password)
        or not re.search("[0-9]{1,}", password)
        or not re.search("["+special_chars+"]{1,}", password)):
        return False

    return True

def is_bad(word):
    if is_valid_password(word) == False:
        return True

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
    print(response)

    count_eval = response['Count'] > 0
    return count_eval

def lambda_handler(event, context):
    # word = event['pathParameters']['word']

    body = json.loads(event['body'])
    word = body['word']
    print('Looking up if {} is a bad password'.format(word))

    is_bad_eval = is_bad(word)

    print('Is {} bad {}'.format(word, is_bad_eval))

    return respond(False, {'response': is_bad_eval})
