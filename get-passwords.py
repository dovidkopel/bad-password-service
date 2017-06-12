#!/usr/bin/python3

import os
import re
from pathlib import PurePath, Path
import boto3
import sys

client = boto3.client('dynamodb')

fetch = True
table = 'bad-passwords'
repo = 'danielmiessler/SecLists.git'
tmp = '/tmp/SecLists'

if len(sys.argv) > 1 and sys.argv[1] == '--no-fetch':
    fetch = False

if len(sys.argv) > 1 and sys.argv[1] != '--no-fetch' and len(sys.argv[1].strip('\s\t')) > 0:
    table = sys.argv[1]
if len(sys.argv) > 2  and len(sys.argv[2].strip('\s\t')) > 0:
    table = sys.argv[2]

print('Fetch is set to {}'.format(fetch))
print('Table is set to {}'.format(table))

def clean_passwords():
    os.system('rm -rf {}'.format(tmp))

def get_passwords():
    os.system('git clone git@github.com:{} {}'.format(repo, tmp))

def get_next(ff):
    return ff.readline().strip('\n\t\r')

def put_password(password):
    if len(password) > 0:
        print('Putting: {}'.format(password))
        client.put_item(
            TableName=table,
            Item={
                'id': {
                    'S': password
                }
            }
        )
    return password

def is_good_password(password):
    if (len(password) < 8
     or not re.search("[A-Z]{1,}", password)
     or not re.search("[a-z]{1,}", password)
     or not re.search("[0-9]{1,}", password)
     or not re.search("[!@#$%^&*?]{1,}", password)):
        return False

    return True

def extract_passwords(p):
    lines = []
    for f in p.iterdir():
        print(f.name)
        ff = f.open()

        try:
            line = get_next(ff)
            while line:
                if len(lines) == 0:
                    if is_good_password(line):
                        lines.append(line)

                line = get_next(ff)
                if is_good_password(line):
                    lines.append(line)


        except UnicodeDecodeError:
            print('no')

    # print(lines)
    return list(set(lines))

def push_passwords(passwords):
    count = 0
    for l in passwords:
        count += 1
        print('Count: {}/{}'.format(count, len(passwords)))
        put_password(l)

if fetch:
    clean_passwords()
    get_passwords()


p = Path('{}/Passwords'.format(tmp))
passwords = extract_passwords(p)
print('There are a total of {} passwords'.format(len(passwords)))
push_passwords(passwords)