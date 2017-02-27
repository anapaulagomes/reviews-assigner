from .reviewsapi import ReviewsAPI


class Assigner:

    def __init__(self):
        self.reviewsapi = ReviewsAPI()

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
        return [language for language in response['application']['languages']]
