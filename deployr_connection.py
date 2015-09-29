#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import requests


class DeployRConnection(object):
    """
    Class to get data from deployr easily...
    """

    def __init__(self, host):
        self.HOST = host
        # Needed for login required requests
        self.JSESSIONID = ""
        self.r_inputs = {}
        self.r_outputs = []

    @classmethod
    def pretty_json(self, json_data):
        return json.dumps(json_data, indent=2)

    def clear_rdata(self):
        # r_inputs and r_outputs have to be removed after api call
        self.r_inputs = {}
        self.r_outputs = []

    def login(self, username, password, disableautosave=True, print_response=True):
        """
        :param username:
        :param password:
        :param disableautosave: boolean
        :param print_response: print log if required
        :return: status code, response data
        """
        if type(username) != str:
            return False, "Username must be string"

        if type(password) != str:
            return False, "Password must be string"

        if type(disableautosave) != bool:
            return False, "Disableautosave must be boolean"

        data = {"username": username, "password": password, "disableautosave": disableautosave}

        status_response, response = self.call_api("r/user/login/", data, print_response=print_response)

        # Store httpcookie if possible
        if status_response and "deployr" in response:
            if "response" in response["deployr"]:
                if "httpcookie" in response["deployr"]["response"]:
                    self.JSESSIONID = response["deployr"]["response"]["httpcookie"]

        return status_response, response

    def set_rinput(self, name, input_type, value):
        """
        Add rinput to be used in next api call
        :param name: key
        :param input_type: variable type
        :param value: value
        :return: True/False, message
        """
        if type(name) != str:
            return False, "Name must be string"

        if type(input_type) != str:
            return False, "Input type must be string"

        self.r_inputs[name] = {"type": input_type, "value": value}

        return True, "Ok"

    def set_routput(self, routput):
        """
        Add routput to be used in next api call
        :param routput: key
        :return: True/False, message
        """
        if type(routput) != str:
            return False, "Routput must be string"

        self.r_outputs.append(routput)

        return True, "Ok"

    def call_api(self, url, data, files={}, print_response=True):
        """
        call api with given parameters and returns its result
        :param url: end point
        :param data: post data
        :param files: files if needed
        :param print_response: print log if required
        :return: status code, response
        """
        if type(url) != str:
            return False, "Url must be string"

        if type(data) != dict:
            return False, "Data must be a dict"

        if type(files) != dict:
            return False, "Files must be a dict"

        if type(print_response) != bool:
            return False, "Print_response must be boolean"

        url = self.HOST + url
        data["format"] = "json"
        cookies = {"JSESSIONID": self.JSESSIONID}

        # Add rinputs to post data
        if self.r_inputs:
            data["inputs"] = json.dumps(self.r_inputs)

        # Add routputs to post data
        if self.r_outputs:
            data["robjects"] = ",".join(self.r_outputs)

        try:
            response = requests.post(url, data=data, files=files, cookies=cookies)
        except requests.exceptions.RequestException as exception:
            self.clear_rdata()
            return 500, {"error": str(exception)}

        status_code = response.status_code

        # Print log only if required
        if print_response:
            print status_code
            print DeployRConnection.pretty_json(response.json())

        # remove rinputs and routputs
        self.clear_rdata()

        return status_code, response.json()
