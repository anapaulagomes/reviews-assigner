from .context import hunter
from hunter import UnauthorizedToken
import mock
import pytest
import requests


@pytest.fixture()
def reviewsapi():
    yield hunter.ReviewsAPI()

@mock.patch('hunter.reviewsapi.requests.get')
def test_retrieve_certifications_list(mock_certifications, reviewsapi):
    projects_list = [{'project_id': 15, 'status': 'certified'},
                    {'project_id': 14, 'status': 'certified'}]

    mock_certifications.return_value.json.return_value = projects_list
    expected_certifications_list = [15, 14]
    certifications_list = reviewsapi.certifications()

    assert certifications_list == expected_certifications_list


@mock.patch('hunter.reviewsapi.requests.get')
def test_retrieve_empty_certifications_list(mock_certifications, reviewsapi):
    mock_certifications.return_value.json.return_value = []
    certifications_list = reviewsapi.certifications()

    assert certifications_list == []


@mock.patch('hunter.reviewsapi.requests.get')
def test_retrieve_certification_list_searching_just_for_certified_projects(mock_certifications, reviewsapi):
    projects_list = [{'project_id': 145, 'status': 'certified'},
                    {'project_id': 15, 'status': 'applied'},
                    {'project_id': 14, 'status': 'certified'}]

    mock_certifications.return_value.json.return_value = projects_list
    expected_certifications_list = [145, 14]
    certifications_list = reviewsapi.certifications()

    assert certifications_list == expected_certifications_list


@mock.patch('hunter.UnauthorizedToken')
@mock.patch('hunter.reviewsapi.requests.get')
def test_unauthorized_url_access_when_try_access_to_certifications_list(mock_certifications, mock_http_error_handler, reviewsapi):
    mock_certifications.return_value.json.side_effect = requests.exceptions.HTTPError()
    mock_http_error_handler.side_effect = UnauthorizedToken()

    with pytest.raises(UnauthorizedToken):
        reviewsapi.certifications()


@mock.patch('hunter.reviewsapi.requests.post')
def test_create_new_request_with_wanted_projects(mock_request, reviewsapi):
    mock_request.status_code = 200
    fake_certifications_list = [42, 57]
    response = reviewsapi.request_reviews(fake_certifications_list)

    assert response.status_code is not None
