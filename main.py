# import argparse
from requests.api import options
import warnings
import argparse
import json
from getpass import getpass
import utils
warnings.filterwarnings('ignore', message='Unverified HTTPS request')
import ticket_get as TicketRequests

MAX_TRIES = 5

def get_details(subdomain = None, username = None, password = None, failed = False):
    if subdomain is None or subdomain=="" or failed:
        subdomain = input("please enter your subdomain\n")
    if username is None or username=="" or failed:
        subdomain = input("please enter your username\n")
    if password is None or password=="" or failed:
        password = getpass("please provide your password\n")
    return {"subdomain":subdomain, "username": username, "password": password}

def get_arguments():
    #Function to get subdomain, username and password from command line
    parser = argparse.ArgumentParser()
    parser.add_argument("--subdomain",type=str, help="enter subdomain xxxxx.zendesk.com (enter only xxx part)")
    parser.add_argument("--username",type=str, help = "enter your username")
    parser.add_argument("--password", type=str, help="enter your password")
    args = parser.parse_args()
    subdomain = args.subdomain
    username = args.username
    password = args.password
    return get_details(subdomain, username, password)

def is_ticket_id_valid(ticket_id):
    try:
        float(ticket_id)
        if float(ticket_id)<0:
            return False
    except ValueError:
        return False
    if len(str(ticket_id).split(" "))>1:
        return False
    return True


if __name__ == "__main__":

    try:
        credentials = get_arguments()
        
        #checking if the credentials are valid 
        valid = TicketRequests.check_validity(credentials)

        # assigning max tries that a user can enter wrong credentials before exiting
        tries = MAX_TRIES

        while valid!=True:
            tries = tries-1
            if tries==0:
                print("!!!!!! YOU HAVE EXCEEDED MAXIMUM NUMBER OF TRIES !!!!!!\n ")
                exit()
            print("\n ENTER VALID CREDENTIALS *****\n")

            # get the credentials again using input command of python
            credentials = get_details(credentials["subdomain"], credentials["username"], credentials["password"], failed=True)
            valid = TicketRequests.check_validity(credentials)
            
        if valid:
            print("\nLogin Successful\n\n Welcome to TicketViewer\n")
            while True:
                print("\t1. List all the tickets in your account")
                print("\t2. Get a specific ticket using ticket id")
                print("\t3. Quit")
                option = input("\nChoose one of the above options\n")

                if option == "3":
                    # quitting the execution if user opts for 3
                    break

                while True:
                    # loop until user enters a valid option
                    if option=="1" or option=="2":
                        break
                    print("1. List all the tickets in your account")
                    print("2. Get a specific ticket using ticket id")
                    option = input("Choose one of the above options\n")

                #option to get all the tickets (paginated to 25 in each page)
                if option == "1":
                    tickets_response = TicketRequests.get_all_tickets(credentials["subdomain"],credentials["username"],credentials["password"])
                    if tickets_response.status_code!=200:
                        
                        if tickets_response.status_code==429:
                            print("\n !!! API call Rate Limit exceeded. Please wait !!!\n")

                        print("\n !!! Something went wrong. Please try again later !!!\n")
                        continue
                    tickets_list = json.loads(tickets_response.text)

                    # loop until user enters a valid next step option
                    while True:
                        parsed_tickets = utils.parse_tickets(tickets_list)
                        print("\n")
                        print(*parsed_tickets, sep="\n")

                        # if there are still tickets in the next page, get the next 25 tickets
                        if tickets_list["meta"]["has_more"]==True:
                            print("")
                            print("\t1. Go to Prev page")
                            print("\t2. Go to next page")
                            print("\t3. Main Menu\n")
                            page = input("Choose one of the above options(1 or 2 or 3)\n")
                            if page == "3":
                                break

                            # get the previous 25 tickets
                            elif page == "1":
                                url = tickets_list["links"]["prev"]
                                tickets_response = TicketRequests.get_all_tickets(credentials["subdomain"],credentials["username"],credentials["password"], url=url)
                                tickets_list = json.loads(tickets_response.text)

                            # get the next 25 tickets
                            elif page == "2":
                                url = tickets_list["links"]["next"]
                                tickets_response = TicketRequests.get_all_tickets(credentials["subdomain"],credentials["username"],credentials["password"], url=url)
                                tickets_list = json.loads(tickets_response.text)
                            else:
                                print("!!! input a valid option (1 or 2 or 3) !!!")
                        else:
                            print("\n END OF TICKETS \n")
                            break
                
                # option to get a specific ticket detail using ticket id
                elif option == "2":
                    ticket_id = input("Please enter a ticket id: \n")
                    while True:
                        if ticket_id!=None and ticket_id!="":

                            if is_ticket_id_valid(ticket_id):
                                break
                            else:
                                ticket_id = input("Please enter a valid ticket id: \n")
                                continue

                        ticket_id = input("Please enter a ticket id: \n")

                    ticket_resp = TicketRequests.get_ticket_details(int(ticket_id),credentials["subdomain"],credentials["username"],credentials["password"])
                    ticket_details = json.loads(ticket_resp.text)
                    # print(ticket_details)
                    if ticket_resp.status_code!=200 and "error" in ticket_details:
                        if ticket_details["error"] == "RecordNotFound":
                            print(f"\n!!!! Ticket with id {ticket_id} doesn't exist!!!!! \n")
                            continue

                    if ticket_resp.status_code!=200:

                        if tickets_response.status_code==429:
                            print("\n !!! API call Rate Limit exceeded. Please wait !!!\n")

                        print("\n\n !!! SOMETHING WENT WRONG. PLEASE TRY AGAIN !!!\n")
                        continue

                    

                    
                    parsed_ticket = utils.form_string(ticket_details["ticket"])
                    print("\n",parsed_ticket,"\n")
                else:
                    print("!!! input a valid option (1 or 2) !!!")

    except KeyboardInterrupt: # exit gracefully if user presses Ctrl+C
        pass
    except:
        print("\n!!! SOMETHING WENT WRONG. PLEASE TRY AGAIN or contact support at abcd@dummy.com !!!\n")
    finally:
        print("\n\tTHANKS FOR USING TICKETVIEWER\n")
