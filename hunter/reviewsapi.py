import requests
import os
from .endpoints import *


class UnauthorizedToken(Exception):
    pass


class ReviewsAPI:

    def __init__(self):
        token = os.environ['UDACITY_AUTH_TOKEN']
        self.headers = {'Authorization': token, 'Content-Length': '0'}

    def go(self, request):
        try:
            raw_response = request()
            response = raw_response.json()

            raw_response.raise_for_status()

            return response
        except requests.exceptions.HTTPError:
            raise UnauthorizedToken('Maybe it\'s time to change you token!')

    def request_certifications(self):
        return requests.get(CERTIFICATIONS_URL, headers=self.headers)

    def certifications(self):
        response = self.go(self.request_certifications)
        return [item['project_id'] for item in response if item['status'] == 'certified']


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
        projects = self.projects_with_languages(certifications_list)
        return requests.post(SUBMISSION_REQUESTS, json=projects, headers=self.headers)

    def projects_with_languages(self, certifications_list):
        languages_list = self.certified_languages()
        projects_list = [{'project_id': project_id, 'language': language} for project_id in certifications_list for language in languages_list]

        return {'projects': projects_list}
