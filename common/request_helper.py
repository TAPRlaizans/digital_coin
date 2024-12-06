import requests
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

class RequestHelper:
    @staticmethod
    def get_response(url, params=None,headers=None):
        try:
            response = requests.get(url, params=params,headers=headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print("requests error:", e)
            return None
        return response
    
    @staticmethod
    def get_response_json(url, params=None,headers=None):
        response = RequestHelper.get_response(url, params=params,headers=headers)
        if response is None:
            print("requests error, is None")
            return None
        return response.json()
    
    @staticmethod
    def get_response_text(url, params=None,headers=None):
        response = RequestHelper.get_response(url, params=params,headers=headers)
        if response is None:
            return None
        return response.text
