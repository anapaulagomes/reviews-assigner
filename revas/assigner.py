from revas.reviewsapi import ReviewsAPI
from datetime import datetime, timedelta
from dateutil import parser
import pytz
import logging
import sys

logging.basicConfig(format='|%(asctime)s| %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Assigner:

    def __init__(self):
        self.reviewsapi = ReviewsAPI()

    def execute(self):
        logger.info('Verifing certified projects...')
        projects = self.projects_with_languages(self.certifications())
        logger.info(projects)
        logger.info('Creating a request ')
        # TODO verify if there is any request before create a new one
        try:
            requests = self.reviewsapi.request_reviews(projects)
        except Exception:
            logger.error('Error opening %s: %s' % (sys.exc_info()[0], sys.exc_info()[1]))

        while True:

            while True:
                if self.has_less_than_the_limit_of_projects_in_review():
                    break
                else:
                    logger.info('Alert! You have 2 reviews to do!')

            active_requests = self.reviewsapi.submission_requests()
            logger.info('Active requests ' + str(active_requests))

            if self.assigned_to_new_review(active_requests):
                logger.info('New Submission!')
                logger.info('Creating a request ')
                try:
                    requests = self.reviewsapi.request_reviews(projects)
                except Exception:
                    logger.error('Error opening %s: %s' % (sys.exc_info()[0], sys.exc_info()[1]))
            # else if needs_refresh(active_requests):
            #      refresh request

            time.sleep(60)


    def certifications(self):
        response = self.reviewsapi.certifications()

        if len(response) < 1:
            raise Exception('You don\'t have any certified project!')
        else:
            return [item['project_id'] for item in response if item['status'] == 'certified']

    def projects_with_languages(self, certifications):
        languages = self.certified_languages()
        projects = [{'project_id': project_id, 'language': language} for project_id in certifications for language in languages]

        return {'projects': projects}

    def certified_languages(self):
        response = self.reviewsapi.certified_languages()

        if len(response['application']['languages']) < 1:
            raise Exception('You don\'t have any certified languages!')
        else:
            return [language for language in response['application']['languages']]

    def has_less_than_the_limit_of_projects_in_review(self):
        limit_of_projects = 2
        response = self.reviewsapi.assigned_count()
        in_review = response['assigned_count']

        return in_review < limit_of_projects

    def active_submission_requests(self):
        return self.reviewsapi.submission_requests()

    def assigned_to_new_review(self, active_requests):
        for active_request in active_requests:
            if active_request['status'] == 'fulfilled':
                return True
        return False

    def needs_refresh(self, active_requests):
        closing_at = parser.parse(active_requests[0]['closed_at'])
        utcnow = datetime.utcnow()
        utcnow = utcnow.replace(tzinfo=pytz.utc)
        return closing_at < utcnow + timedelta(minutes=30)
