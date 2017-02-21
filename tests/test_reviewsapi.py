from .context import hunter
from hunter import UnauthorizedToken
import mock
import pytest
import requests


@mock.patch('hunter.reviewsapi.requests.get')
def test_retrieve_certifications_list(mock_certifications):
    projects_list = [{'project_id': 15, 'status': 'certified'},
                    {'project_id': 14, 'status': 'certified'}]

    mock_certifications.return_value.json.return_value = projects_list

    expected_certifications_list = [15, 14]

    reviewsapi = hunter.ReviewsAPI()
    certifications_list = reviewsapi.certifications()

    assert certifications_list == expected_certifications_list


@mock.patch('hunter.reviewsapi.requests.get')
def test_retrieve_empty_certifications_list(mock_certifications):
    mock_certifications.return_value.json.return_value = []

    reviewsapi = hunter.ReviewsAPI()
    certifications_list = reviewsapi.certifications()

    assert certifications_list == []


@mock.patch('hunter.reviewsapi.requests.get')
def test_retrieve_certification_list_searching_just_for_certified_projects(mock_certifications):
    projects_list = [{'project_id': 145, 'status': 'certified'},
                    {'project_id': 15, 'status': 'applied'},
                    {'project_id': 14, 'status': 'certified'}]

    mock_certifications.return_value.json.return_value = projects_list

    expected_certifications_list = [145, 14]

    reviewsapi = hunter.ReviewsAPI()
    certifications_list = reviewsapi.certifications()

    assert certifications_list == expected_certifications_list


@mock.patch('hunter.UnauthorizedToken')
@mock.patch('hunter.reviewsapi.requests.get')
def test_unauthorized_url_access_when_try_access_to_certifications_list(mock_certifications, mock_http_error_handler):
    mock_certifications.return_value.json.side_effect = requests.exceptions.HTTPError()
    mock_http_error_handler.side_effect = UnauthorizedToken()

    reviewsapi = hunter.ReviewsAPI()

    with pytest.raises(UnauthorizedToken):
        reviewsapi.certifications()


@mock.patch('hunter.reviewsapi.requests.post')
def test_create_new_request_with_wanted_projects(mock_request):
    mock_request.status_code = 200

    fake_certifications_list = [42, 57]

    reviewsapi = hunter.ReviewsAPI()
    response = reviewsapi.request_reviews(fake_certifications_list)

    assert response.status_code is not None
