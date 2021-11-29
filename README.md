# Zendesk Coding Challenge

A command line interface to view Zendesk tickets 

### Technical Stack

Developed with Python 3.9 (Should work with Python 3.x)

### Requirement

1. requests (pip install requests)
2. argparse (pip install argparse)

## Usage

Run the code with
```python main.py --subdomain {subdomain} --username {username} --password {password}```
If your subdomain is xxxx.zendesk.com, then enter {subdomain} as xxxx
and provide your {username} and {password} to connect to the application

If invalid credentials are provided, you will be prompted again to enter correct credentials

## Tests

Run tests with
```python tests.py```

## Features
1. Displays tickets using Zendesk API for a particular account
2. Pagination implemented to view 25 tickets at once, with options to go to next and prev 25 tickets
3. Option to view specific ticket detail using ticket_id

