# from dateutil import parser
from datetime import datetime

def format_datetime(created_at):
    dt = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")
    created_time = "%d-%d-%d %d:%d:%d" % (dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
    return created_time

def form_string(ticket):
    # created_at = parser.parse(ticket["created_at"])
    created_at = format_datetime(ticket["created_at"])
    ticket_string = f"Ticket id: {ticket['id']} with subject {ticket['subject']} opened by {ticket['submitter_id']} and requested by {ticket['requester_id']} on {created_at}"
    return ticket_string

def parse_tickets(json_ticket_data):
    resp = []
    if "tickets" not in json_ticket_data:
        return []
    for ticket in json_ticket_data["tickets"]:
        ticket_string = form_string(ticket)
        resp.append(ticket_string)
    return resp


    
