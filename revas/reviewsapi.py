import requests
import os
from revas.endpoints import *
import sys
import traceback


class UnauthorizedToken(Exception):
    pass


class ReviewsAPI:

    def __init__(self):
        token = os.environ['UDACITY_AUTH_TOKEN']
        self.headers = {'Authorization': token, 'Content-Length': '0'}

    def execute(self, request):
        try:
            raw_response = request()
            # TODO before raise an exception to verify if there is a {'error': 'message'}
            response = raw_response.json()
            raw_response.raise_for_status()

            return response
        except requests.exceptions.HTTPError:
            print('Error opening %s: %s || %s' % (sys.exc_info()[0], sys.exc_info()[1], traceback.format_exc()))
            raise UnauthorizedToken('Maybe it\'s time to change your token!')

    def certifications(self):
        return self.execute(lambda: requests.get(CERTIFICATIONS, headers=self.headers))

    def certified_languages(self):
        return self.execute(lambda: requests.get(REVIEWER, headers=self.headers))

    def request_reviews(self, projects):
        return self.execute(lambda: requests.post(NEW_SUBMISSION_REQUESTS, headers=self.headers, json=projects))

    def assigned_count(self):
        return self.execute(lambda: requests.get(ASSIGNED_COUNT, headers=self.headers))

    def submission_requests(self):
        return self.execute(lambda: requests.get(SUBMISSION_REQUESTS, headers=self.headers))

    def refresh_request(self, request_id):
        return self.execute(lambda: requests.put(REQUEST_REFRESH.format(BASE_URL, request_id), headers=self.headers))
