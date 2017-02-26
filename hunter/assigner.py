from .reviewsapi import ReviewsAPI


class Assigner:

    def __init__(self):
        self.reviewsapi = ReviewsAPI()

    def certifications(self):
        response = self.reviewsapi.certifications()
        return [item['project_id'] for item in response if item['status'] == 'certified']

    def projects_with_languages(self, certifications):
        languages = self.reviewsapi.certified_languages()
        projects = [{'project_id': project_id, 'language': language} for project_id in certifications for language in languages]

        return {'projects': projects}
