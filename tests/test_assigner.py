from .context import hunter
from hunter import UnauthorizedToken
import os
import mock
import pytest


@pytest.fixture()
def assigner():
    os.environ['UDACITY_AUTH_TOKEN'] = 'some auth token'
    yield hunter.Assigner()


@mock.patch('hunter.reviewsapi.ReviewsAPI.certifications')
def test_retrieve_certifications_list(mock_certifications, assigner):
    projects_list = [{'project_id': 15, 'status': 'certified'},
                    {'project_id': 14, 'status': 'certified'}]

    mock_certifications.return_value.ok = True
    mock_certifications.return_value = projects_list
    expected_certifications_list = [15, 14]
    certifications_list = assigner.certifications()

    assert certifications_list == expected_certifications_list


@mock.patch('hunter.reviewsapi.ReviewsAPI.certifications')
def test_retrieve_certification_list_searching_just_for_certified_projects(mock_certifications, assigner):
    projects_list = [{'project_id': 145, 'status': 'certified'},
                    {'project_id': 15, 'status': 'applied'},
                    {'project_id': 14, 'status': 'certified'}]

    mock_certifications.return_value.ok = True
    mock_certifications.return_value = projects_list
    expected_certifications_list = [145, 14]
    certifications_list = assigner.certifications()

    assert certifications_list == expected_certifications_list


@mock.patch('hunter.reviewsapi.ReviewsAPI.certifications')
def test_retrieve_empty_certifications_list(mock_certifications, assigner):
    mock_certifications.return_value.ok = True
    mock_certifications.return_value = []
    certifications_list = assigner.certifications()

    assert certifications_list == []
