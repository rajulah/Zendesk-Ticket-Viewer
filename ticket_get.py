import requests
from requests.auth import HTTPBasicAuth
import warnings
warnings.filterwarnings('ignore', message='Unverified HTTPS request')

def get_all_tickets(subdomain: str, username: str, password: str, url: str = None):
    # getting the tickets list 25 at a time
    if url is None:
        url = f"https://{subdomain}.zendesk.com/api/v2/tickets?page[size]=25"
    response = requests.get(url, verify=False, auth=HTTPBasicAuth(username, password))
    return response




def get_ticket_details(ticket_id: int, subdomain: str, username: str, password: str):
    # getting single ticket details using ticket id
    url = f"https://{subdomain}.zendesk.com/api/v2/tickets/{ticket_id}"
    response = requests.get(url, verify=False, auth=HTTPBasicAuth(username, password))
    return response

def check_validity(credentials):
    # checking if the credentials provided are valid
    res = get_all_tickets(credentials["subdomain"], credentials["username"],credentials["password"])
    if res.status_code and res.status_code==200:
        return True
    else:
        return False