from .context import revas
from revas import UnauthorizedToken
import os
import mock
import pytest


@pytest.fixture()
def assigner():
    os.environ['UDACITY_AUTH_TOKEN'] = 'some auth token'
    yield revas.Assigner()


@mock.patch('revas.reviewsapi.ReviewsAPI.certifications')
def test_retrieve_certifications_list(mock_certifications, assigner):
    projects_list = [{'project_id': 15, 'status': 'certified'},
                    {'project_id': 14, 'status': 'certified'}]

    mock_certifications.return_value.ok = True
    mock_certifications.return_value = projects_list
    expected_certifications_list = [15, 14]
    certifications_list = assigner.certifications()

    assert certifications_list == expected_certifications_list


@mock.patch('revas.reviewsapi.ReviewsAPI.certifications')
def test_retrieve_certification_list_searching_just_for_certified_projects(mock_certifications, assigner):
    projects_list = [{'project_id': 145, 'status': 'certified'},
                    {'project_id': 15, 'status': 'applied'},
                    {'project_id': 14, 'status': 'certified'}]

    mock_certifications.return_value.ok = True
    mock_certifications.return_value = projects_list
    expected_certifications_list = [145, 14]
    certifications_list = assigner.certifications()

    assert certifications_list == expected_certifications_list


@mock.patch('revas.reviewsapi.ReviewsAPI.certifications')
def test_raise_an_exception_when_return_empty_certifications_list(mock_certifications, assigner):
    mock_certifications.return_value.ok = True
    mock_certifications.return_value = []

    with pytest.raises(Exception):
        assigner.certifications()


@mock.patch('revas.assigner.Assigner.certified_languages')
def test_should_return_projects_with_certified_languages(mock_certified_languages, assigner):
    expected_languages = ['en-us', 'zh-cn', 'pt-br']
    mock_certified_languages.return_value.ok = True
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

    projects_with_languages = assigner.projects_with_languages(certifications_list)

    assert len(projects_with_languages) == len(expected_projects_with_languages)


@mock.patch('revas.reviewsapi.ReviewsAPI.certified_languages')
def test_should_return_certified_languages(mock_certified_languages, assigner):
    mock_certified_languages.return_value.ok = True
    mock_certified_languages.return_value = {'application': {'languages': ['en-us', 'zh-cn', 'pt-br']}}
    expected_certified_languages = ['en-us', 'zh-cn', 'pt-br']

    languages = assigner.certified_languages()
    assert languages == expected_certified_languages


@mock.patch('revas.reviewsapi.ReviewsAPI.certified_languages')
def test_raise_an_exception_when_return_empty_certified_languages_list(mock_certified_languages, assigner):
    mock_certified_languages.return_value.ok = True
    mock_certified_languages.return_value = {'application': {'languages': []}}

    with pytest.raises(Exception):
        assigner.certified_languages()
