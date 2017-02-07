from .context import hunter
import mock


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
