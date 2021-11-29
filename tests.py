import unittest
import base64

from ticket_get import *
from main import *
from utils import *
import json
import warnings
warnings.filterwarnings('ignore', message='Unverified HTTPS request')


username = "rajulah@gmail.com"
subdomain = "zccharishrajula"
encoded_password = "aWlJdEAxMjM0"
password = base64.b64decode(encoded_password).decode('utf-8')

class TestTicketViewer(unittest.TestCase):

	def test_get_all_tickets(self):
		f = open('test_data_all.json', "r")
		data = json.loads(f.read())
		f.close()
		resp = get_all_tickets(subdomain,username,password)
		resp = json.loads(resp.text)
		self.assertEqual(resp,data)

		invalid_credentials = get_all_tickets(subdomain,username,"wrongpassword")
		self.assertEqual(401,invalid_credentials.status_code)




	def test_get_ticket_details(self):
		f = open('test_data_single.json', "r")
		data = json.loads(f.read())
		f.close()
		resp = get_ticket_details(ticket_id=2,subdomain=subdomain,username=username,password=password)
		resp = json.loads(resp.text)
		self.assertEqual(resp,data)

		invalid_ticket_id = get_ticket_details(ticket_id=2000,subdomain=subdomain,username=username,password=password)
		invalid_ticket_id = json.loads(invalid_ticket_id.text)
		self.assertEqual("RecordNotFound",invalid_ticket_id["error"])

class UtilsTests(unittest.TestCase):

	def test_format_datetime(self):
		raw_date = '2021-11-28T18:29:10Z'
		formatted_date = format_datetime(raw_date)
		self.assertTrue(str(formatted_date) == '2021-11-28 18:29:10')

	def test_form_string(self):
		f = open('test_data_single.json', "r")
		ticket = json.loads(f.read())
		f.close()
		self.assertEqual("Ticket id: 2 with subject velit eiusmod reprehenderit officia cupidatat opened by 1903564032647 and requested by 1903564032647 on 2021-11-24 19:31:13",form_string(ticket["ticket"]))

class MainTests(unittest.TestCase):

	def test_is_ticket_id_valid(self):
		self.assertTrue(is_ticket_id_valid("2"))
		self.assertTrue(is_ticket_id_valid("25"))
		self.assertTrue(is_ticket_id_valid(5))

		self.assertFalse(is_ticket_id_valid(-5))
		self.assertFalse(is_ticket_id_valid("2 5"))
		self.assertFalse(is_ticket_id_valid("abcd"))
		self.assertFalse(is_ticket_id_valid("5 abcd"))
		self.assertFalse(is_ticket_id_valid("-5"))
		
	





if __name__ == '__main__':
	unittest.main()