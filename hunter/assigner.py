from .reviewsapi import ReviewsAPI


class Assigner:

    def __init__(self):
        self.reviewsapi = ReviewsAPI()

    def certifications(self):
        response = self.reviewsapi.certifications()
        return [item['project_id'] for item in response if item['status'] == 'certified']

    def projects_with_languages(self, certifications_list):
        languages_list = self.reviewsapi.certified_languages()
        projects_list = [{'project_id': project_id, 'language': language} for project_id in certifications_list for language in languages_list]

        return {'projects': projects_list}
