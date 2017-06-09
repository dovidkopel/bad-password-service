# Bad Password Service

# Libraries
You must have Python 3.6, `boto3`, `pathlib`

# AWS
This tool expects the current environment to have at least this policy:
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "dynamodb:PutItem"
            ],
            "Resource": [
                "arn:aws:dynamodb:{REGION}:{ACCOUNT}:table/{TABLE}"
            ]
        }
    ]
}
```

Replacing region, account and table accordingly.
 
# Lambda
Role should have a policy like this:
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "dynamodb:Query"
            ],
            "Resource": [
                "arn:aws:dynamodb:{REGION}:{ACCOUNT}:table/{TABLE}"
            ]
        }
    ]
}
```

Replacing region, account and table accordingly.

# Free service
We have a free endpoint to use this service if you want.

```
curl -X POST \
  https://bad-passwords.getbabyscripts.com/ \
  -H 'content-type: application/json' \
  -d '{
    "word": "foobar"
}'
```

If the supplied word is in fact a bad password then the body will have the key `response` set to `true`.