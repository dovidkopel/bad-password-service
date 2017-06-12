# Bad Password Service

# Libraries
You must have Python 3.6, `boto3`, `pathlib`

# Getting passwords
Run the `get-passwords.py` script to obtain the passwords. 
By default the script will obtain the passwords from the github repo provided.
It's a fairly simple script. Add the `--no-fetch` option to not obtain the password.
`python3 get-passwords.py --no-fetch`
The default dynamodb table is `bad-passwords` you may either manually change it in the script or pass it on the command line.
`python3 get-passwords.py my-table`

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
You may use the *https://bad-passwords.getbabyscripts.com* endpoint.

We now filtered out any invalid passwords prior to querying the bad passwords database.
```
curl -X POST \
  https://bad-passwords.getbabyscripts.com/ \
  -H 'content-type: application/json' \
  -d '{
    "word": "foobar"
}'
```

If the supplied word is in fact a bad password then the body will have the key `response` set to `true`.