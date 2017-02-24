import requests
import os
from .endpoints import *


class UnauthorizedToken(Exception):
    pass


class ReviewsAPI:

    def __init__(self):
        token = os.environ['UDACITY_AUTH_TOKEN']
        self.headers = {'Authorization': token, 'Content-Length': '0'}

    def certifications(self):
        try:
            raw_response = requests.get(CERTIFICATIONS_URL, headers=self.headers)
            response = raw_response.json()

            raw_response.raise_for_status()

            certifications_list = [item['project_id'] for item in response if item['status'] == 'certified']
            return certifications_list
        except requests.exceptions.HTTPError:
            raise UnauthorizedToken('Maybe it\'s time to change you token!')

    def certified_languages(self):
        try:
            raw_response = requests.get(REVIEWER_URL, headers=self.headers)
            response = raw_response.json()

            raw_response.raise_for_status()
            
            languages_list = [language for language in response['application']['languages']]

            return languages_list
        except requests.exceptions.HTTPError:
            raise UnauthorizedToken('Maybe it\'s time to change you token!')

    def request_reviews(self, certifications_list):
        projects = self.__format_projects(certifications_list)
        return requests.post(SUBMISSION_REQUESTS, json=projects, headers=self.headers)

    # TODO Add support to multi language
    def __format_projects(self, certifications_list):
        projects_list = []
        for certification in certifications_list:
            projects_list.append({'project_id': certification, 'language': 'pt-br'})
        return {'projects': projects_list}
