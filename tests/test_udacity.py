from .context import hunter
from hunter import UnauthorizedToken
import mock
import pytest
import requests


@mock.patch('hunter.udacity.requests.get')
def test_retrieve_certifications_list(mock_certifications):
    projects_list = [{'project_id': 15, 'status': 'certified'},
                    {'project_id': 14, 'status': 'certified'}]

    mock_certifications.return_value.json.return_value = projects_list

    udacity = hunter.UdacityConnection()
    assert udacity.certifications() == [15, 14]


@mock.patch('hunter.udacity.requests.get')
def test_retrieve_empty_certifications_list(mock_certifications):
    mock_certifications.return_value.json.return_value = []

    udacity = hunter.UdacityConnection()
    assert udacity.certifications() == []


@mock.patch('hunter.udacity.requests.get')
def test_retrieve_certification_list_searching_just_for_certified_projects(mock_certifications):
    projects_list = [{'project_id': 145, 'status': 'certified'},
                    {'project_id': 15, 'status': 'applied'},
                    {'project_id': 14, 'status': 'certified'}]

    mock_certifications.return_value.json.return_value = projects_list

    udacity = hunter.UdacityConnection()
    assert udacity.certifications() == [145, 14]


@mock.patch('hunter.UnauthorizedToken')
@mock.patch('hunter.udacity.requests.get')
def test_unauthorized_url_access_when_try_access_to_certifications_list(mock_certifications, mock_http_error_handler):
    mock_certifications.return_value.json.side_effect = requests.exceptions.HTTPError()
    mock_http_error_handler.side_effect = UnauthorizedToken()

    udacity = hunter.UdacityConnection()

    with pytest.raises(UnauthorizedToken):
        udacity.certifications()
