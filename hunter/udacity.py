import requests
import os


class UnauthorizedToken(Exception):
    pass


class UdacityConnection:

    def __init__(self):
        self.certifications_url = 'https://review-api.udacity.com/api/v1/me/certifications.json'
        token = os.environ.get('UDACITY_AUTH_TOKEN')
        self.headers = {'Authorization': token, 'Content-Length': '0'}

    def certifications(self):
        try:
            raw_response = requests.get(self.certifications_url, headers=self.headers)
            response = raw_response.json()
            certifications_list = [item['project_id'] for item in response if item['status'] == 'certified']
            return certifications_list
        except requests.exceptions.HTTPError:
            raise UnauthorizedToken

    def request_reviews(self, certifications_list):
        projects = self.__projects(certifications_list)
        return requests.post('https://review-api.udacity.com/api/v1/submission_requests.json', json=projects, headers=self.headers)

    # TODO Add support to multi language
    def __projects(self, certifications_list):
        projects_list = []
        for certification in certifications_list:
            projects_list.append({'project_id': certification, 'language': 'pt-br'})
        return {'projects': projects_list}
