from .context import hunter
from hunter import UnauthorizedToken
from hunter import endpoints
import os
import mock
from mock import ANY
import pytest
import requests


@pytest.fixture()
def reviewsapi():
    os.environ['UDACITY_AUTH_TOKEN'] = 'some auth token'
    yield hunter.ReviewsAPI()


@mock.patch('hunter.reviewsapi.requests.get')
def test_retrieve_certifications_list(mock_certifications, reviewsapi):
    expected_response = [{
                    "id": 0,
                    "status": "applied",
                    "active": True,
                    "created_at": "string",
                    "updated_at": "string",
                    "waitlisted_at": "string",
                    "certified_at": "string",
                    "project_id": 0,
                    "grader_id": 0,
                    "trainings_count": 0,
                    "project": {
                      "id": 0,
                      "name": "string",
                      "required_skills": "string",
                      "awaiting_review_count": 0,
                      "hashtag": "string",
                      "visible": True,
                      "audit_rubric_id": 0
                    }
                  }
                ]

    mock_certifications.return_value.ok = True
    mock_certifications.return_value.json.return_value = expected_response
    certifications_response = reviewsapi.certifications()

    mock_certifications.assert_called_once_with(endpoints.CERTIFICATIONS_URL, headers=ANY)
    assert certifications_response == expected_response


@mock.patch('hunter.reviewsapi.requests.get')
def test_retrieve_certified_languages_to_perform_reviews(mock_review_profile, reviewsapi):
    languages = {'application': {'languages': ['en-us', 'zh-cn', 'pt-br']}}

    mock_review_profile.return_value.ok = True
    mock_review_profile.return_value.json.return_value = languages
    expected_languages_list = ['en-us', 'zh-cn', 'pt-br']
    languages_list = reviewsapi.certified_languages()

    assert languages_list == expected_languages_list


@mock.patch('hunter.reviewsapi.ReviewsAPI.certified_languages')
def test_should_return_projects_with_certified_languages(mock_certified_languages, reviewsapi):
    expected_languages = ['en-us', 'zh-cn', 'pt-br']
    mock_certified_languages.return_value = expected_languages
    certifications_list = [1, 2, 3]
    expected_projects_with_languages = {'projects':
                                        [{'project_id': certifications_list[0], 'language': expected_languages[0]},
                                        {'project_id': certifications_list[0], 'language': expected_languages[1]},
                                        {'project_id': certifications_list[0], 'language': expected_languages[2]},
                                        {'project_id': certifications_list[1], 'language': expected_languages[0]},
                                        {'project_id': certifications_list[1], 'language': expected_languages[1]},
                                        {'project_id': certifications_list[1], 'language': expected_languages[2]},
                                        {'project_id': certifications_list[2], 'language': expected_languages[0]},
                                        {'project_id': certifications_list[2], 'language': expected_languages[1]},
                                        {'project_id': certifications_list[2], 'language': expected_languages[2]}]}

    projects_with_languages = reviewsapi.projects_with_languages(certifications_list)

    assert len(projects_with_languages) == len(expected_projects_with_languages)


@mock.patch('hunter.UnauthorizedToken')
@mock.patch('hunter.reviewsapi.requests.get')
def test_unauthorized_url_access_when_try_access_to_certifications_list(mock_certifications, mock_http_error_handler, reviewsapi):
    mock_certifications.return_value.ok = False
    mock_certifications.return_value.json.side_effect = requests.exceptions.HTTPError()
    mock_http_error_handler.side_effect = UnauthorizedToken()

    with pytest.raises(UnauthorizedToken):
        reviewsapi.certifications()


@mock.patch('hunter.reviewsapi.requests.get')
def test_should_throw_an_exception_when_status_code_is_different_of_2xx(mock_request, reviewsapi):
    http_error = requests.exceptions.HTTPError()
    mock_request.return_value.ok = False
    mock_request.return_value.raise_for_status.side_effect = http_error

    with pytest.raises(Exception):
        reviewsapi.certifications()


@mock.patch('hunter.reviewsapi.requests.get')
def test_should_throw_an_exception_when_happens_a_network_problem(mock_request, reviewsapi):
    http_error = requests.exceptions.ConnectionError()
    mock_request.return_value.ok = False
    mock_request.return_value.raise_for_status.side_effect = http_error

    with pytest.raises(Exception):
        reviewsapi.certifications()

@mock.patch('hunter.reviewsapi.ReviewsAPI.projects_with_languages')
@mock.patch('hunter.reviewsapi.requests.post')
def test_create_new_request_with_wanted_projects(mock_request, mock_projects_with_languages, reviewsapi):
    expected_languages = ['en-us', 'zh-cn', 'pt-br']
    mock_projects_with_languages.return_value = expected_languages
    mock_request.return_value.ok = True

    fake_certifications_list = [42, 57]
    response = reviewsapi.request_reviews(fake_certifications_list)

    mock_request.assert_called_once_with(endpoints.SUBMISSION_REQUESTS_URL, headers=ANY, json=ANY)
    assert response.status_code is not None
