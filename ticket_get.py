import requests
import json
from requests.auth import HTTPBasicAuth
from getpass import getpass


def get_all_tickets(subdomain: str, username: str, password: str, url: str = None):
    if url is None:
        url = f"https://{subdomain}.zendesk.com/api/v2/tickets?page[size]=25"
    response = requests.get(url, verify=False, auth=HTTPBasicAuth(username, password))
    # print(response)
    return response
    # if response.status_code==200:
    #     return response
    # else:
    #     print("authentication failed")



def get_ticket_details(ticket_id: int, subdomain: str, username: str, password: str):
    url = f"https://{subdomain}.zendesk.com/api/v2/tickets/{ticket_id}"
    response = requests.get(url, verify=False, auth=HTTPBasicAuth(username, password))
    # print(response)
    return response


def get_details(subdomain = None, username = None, password = None, failed = False):
    if subdomain is None or subdomain=="" or failed:
        subdomain = input("please enter your subdomain\n")
    if username is None or username=="" or failed:
        subdomain = input("please enter your username\n")
    if password is None or password=="" or failed:
        password = getpass("please provide your password\n")
    return {"subdomain":subdomain, "username": username, "password": password}

def check_validity(credentials):
    res = get_all_tickets(credentials["subdomain"], credentials["username"],credentials["password"])
    if res.status_code and res.status_code==200:
        return True
    else:
        return False