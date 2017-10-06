# -*- coding: utf-8 -*-

'''Python module to work with Atlassian Cloud API'''

import json
import logging
from urllib.parse import urlencode, urljoin
import requests

class AtlassianCloudRestAPI:
    '''Connection object to Atlassian Cloud API'''
    def __init__(self, url, session=requests.Session()):
        self.session = session
        self.url = url


    def request(self, method='GET', path='/', data=None, params=None, files=None, headers=None):
        '''Base request method'''
        if headers is None:
            headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        if data is not None:
            data = json.dumps(data)
        url = urljoin(self.url, path)
        response = self.session.request(
            method=method,
            url=url,
            params=params,
            headers=headers,
            files=files,
            data=data,
            timeout=60,
        )
        if response.status_code == 200:
            logging.debug('Received: %s', response.json())
        elif response.status_code == 204:
            logging.debug('Received "204 No Content" response')
        else:
            logging.info(response.json())
            response.raise_for_status()
        return response


    def get(self, path, data=None, params=None, headers=None):
        '''GET method'''
        if headers is None:
            headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        return self.request('GET', path=path, params=params, data=data, headers=headers).json()


    def post(self, path, data=None, files=None, headers=None):
        '''POST method'''
        if headers is None:
            headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        try:
            return self.request('POST', path=path, data=data, files=files, headers=headers).json()
        except ValueError:
            logging.debug('Received response with no content')
            return None


    def put(self, path, data=None, headers=None):
        '''PUT method'''
        if headers is None:
            headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        try:
            return self.request('PUT', path=path, data=data, headers=headers).json()
        except ValueError:
            logging.debug('Received response with no content')
            return None


    def delete(self, path, data=None, headers=None):
        '''DELETE method'''
        if headers is None:
            headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        self.request('DELETE', path=path, data=data, headers=headers)


    def auth(self, username, password):
        '''Initiate cookie based auth with Atlassian ID system'''
        data = {
            'username': username,
            'password': password,
        }
        logging.info('Requesting cookie based authentication for %s', username)
        req = self.request('POST', path='/rest/auth/1/session', data=data)
        logging.debug('Auth request returned %s', req.status_code)
        return req.status_code == 200
