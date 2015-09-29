import unittest
from mock import patch, Mock
from deployr_connection import DeployRConnection


class RequestsResponseMockObject(object):
	status_code = 200

	def __init__(self, resp):
		self.response = resp

	def json(self):
		return self.response


class DeployRConnectionTest(unittest.TestCase):

	def setUp(self):
		self.deployr_connection = DeployRConnection("some.host/api/")

	# .set_rinput(self, name, input_type, value)
	def test_set_rinput(self):
		status, response = self.deployr_connection.set_rinput("name", "primitive", 7)

		self.assertTrue(status)
		self.assertEquals(response, "Ok")
		self.assertEquals(len(self.deployr_connection.r_inputs), 1)

	def test_set_rinput_bad_variable_name(self):
		status, response = self.deployr_connection.set_rinput(7, "primitive", 7)

		self.assertFalse(status)
		self.assertEquals(response, "Name must be string")
		self.assertEquals(len(self.deployr_connection.r_inputs), 0)

	def test_set_rinput_bad_input_type(self):
		status, response = self.deployr_connection.set_rinput("name", [], 7)

		self.assertFalse(status)
		self.assertEquals(response, "Input type must be string")
		self.assertEquals(len(self.deployr_connection.r_inputs), 0)

	# .set_routput(self, routput)
	def test_set_routput(self):
		status, response = self.deployr_connection.set_routput("variable_name")

		self.assertTrue(status)
		self.assertEquals(response, "Ok")
		self.assertEquals(len(self.deployr_connection.r_outputs), 1)

	def test_set_routput_bad_variable_name(self):
		status, response = self.deployr_connection.set_routput(7)

		self.assertFalse(status)
		self.assertEquals(response, "Routput must be string")
		self.assertEquals(len(self.deployr_connection.r_outputs), 0)

	# .login(self, username, password, disableautosave=True, print_response=True)
	def test_login(self):
		response_for_login = {"deployr": { "response": { "httpcookie": "D0853BD6A024BC7C3795DDCCC6B4FEF3"} } }

		patch('requests.post', Mock(return_value=RequestsResponseMockObject(response_for_login))).start()

		status, response = self.deployr_connection.login("admin", "123456", print_response=False)

		self.assertTrue(status)
		self.assertEquals(response, response_for_login)
		self.assertNotEquals(self.deployr_connection.JSESSIONID, "")

	def test_login_bad_username(self):
		status, response = self.deployr_connection.login(7, "123456")

		self.assertFalse(status)
		self.assertEquals(response, "Username must be string")

	def test_login_bad_password(self):
		status, response = self.deployr_connection.login("admin", 123456)

		self.assertFalse(status)
		self.assertEquals(response, "Password must be string")

	# .call_api(self, url, data, files={}, print_response=True)
	def test_call_api(self):
		response_for_login = {"deployr": { "response": { "success": True} } }

		patch('requests.post', Mock(return_value=RequestsResponseMockObject(response_for_login))).start()

		status, response = self.deployr_connection.call_api("some/end/point/", {'key': 'value'}, print_response=False)

		self.assertTrue(status)
		self.assertEquals(response, response_for_login)

	def test_call_api_with_rinputs_and_routputs(self):
		response_for_login = {"deployr": { "response": { "success": True} } }

		patch('requests.post', Mock(return_value=RequestsResponseMockObject(response_for_login))).start()

		self.deployr_connection.set_rinput("name", "primitive", 7)
		self.deployr_connection.set_rinput("name", "primitive", 8)
		self.deployr_connection.set_routput("variable_name")

		status, response = self.deployr_connection.call_api("some/end/point/", {'key': 'value'}, print_response=False)

		self.assertTrue(status)
		self.assertEquals(response, response_for_login)
		self.assertEquals(len(self.deployr_connection.r_inputs), 0)
		self.assertEquals(len(self.deployr_connection.r_outputs), 0)

	def test_call_api_bad_url(self):
		status, response = self.deployr_connection.call_api(123, {})

		self.assertFalse(status)
		self.assertEquals(response, "Url must be string")

	def test_call_api_bad_data(self):
		status, response = self.deployr_connection.call_api("some/end/point/", "{'key': 'value'}")

		self.assertFalse(status)
		self.assertEquals(response, "Data must be a dict")

	def test_call_api_bad_files(self):
		status, response = self.deployr_connection.call_api("some/end/point/", {}, "{'key': 'value'}")

		self.assertFalse(status)
		self.assertEquals(response, "Files must be a dict")

	def test_call_api_bad_print_response(self):
		status, response = self.deployr_connection.call_api("some/end/point/", {}, print_response="True")

		self.assertFalse(status)
		self.assertEquals(response, "Print_response must be boolean")
