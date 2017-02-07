import requests
import os


class UdacityConnection:

    def __init__(self):
        self.certifications_url = 'https://review-api.udacity.com/api/v1/me/certifications.json'
        token = os.environ.get('UDACITY_AUTH_TOKEN')
        self.headers = {'Authorization': token, 'Content-Length': '0'}

    def certifications(self):
        response = requests.get(self.certifications_url, headers=self.headers).json()
        certifications_list = [item['project_id'] for item in response if item['status'] == 'certified']
        return certifications_list
