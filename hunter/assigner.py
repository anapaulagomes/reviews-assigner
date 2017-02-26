from .reviewsapi import ReviewsAPI


class Assigner:

    def __init__(self):
        self.reviewsapi = ReviewsAPI()

    def certifications(self):
        response = self.reviewsapi.certifications()
        return [item['project_id'] for item in response if item['status'] == 'certified']
