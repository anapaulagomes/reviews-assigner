# Review's Assigner

Assign Udacity's revision automatically! 🔦 [![Build Status](https://travis-ci.org/anapaulagomes/reviews-assigner.svg?branch=master)](https://travis-ci.org/anapaulagomes/reviews-assigner) [![Code Climate](https://codeclimate.com/github/anapaulagomes/reviews-assigner/badges/gpa.svg)](https://codeclimate.com/github/anapaulagomes/reviews-assigner)

This project is focused on Udacity's reviewer. Considering this, you should have an _auth token_.
Add it as environment variable with the name `UDACITY_AUTH_TOKEN`.

### Creating new environment

This project has been developed with Python 3.6 but it's has been tested with versions 2.7 and 3.4.

To create a new environment execute `python3 -m venv venv`. Make sure to config your _auth token_ in `venv/bin/activate` file. To activate run `source venv/bin/activate` and to deactivate run `source deactivate`.

### Tests

Running tests with _pytest_ it's pretty easy: `pytest tests`. You may check tests coverage with `pytest --cov=revas/ tests` and the "flakes" (errors) with `flake8 revas/`.

You can perform search on API using: `curl -X GET -H "Authorization: $UDACITY_AUTH_TOKEN" -H "Content-Length: 0" https://review-api.udacity.com/api/v1/me/submission_requests.json`

To create a new request:

```curl -X POST -H "Authorization: $UDACITY_AUTH_TOKEN" --header 'Content-Type: application/json' --header 'Accept: application/json' -d '{"projects": [{"project_id": 145, "language": "pt"}, {"project_id": 134, "language": "pt"}, {"project_id": 151, "language": "pt"}, {"project_id": 47, "language": "pt"}, {"project_id": 8, "language": "pt"}, {"project_id": 83, "language": "pt"}]}' 'https://review-api.udacity.com/api/v1/submission_requests'```
