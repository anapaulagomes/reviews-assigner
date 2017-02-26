# Review's Assigner

Assign Udacity's revision automatically! 🔦 [![Build Status](https://travis-ci.org/anapaulagomes/review-hunter.svg?branch=master)](https://travis-ci.org/anapaulagomes/review-hunter)

This project is focused on Udacity's reviewer. Considering this, you should have an _auth token_.
Add it as environment variable with the name `UDACITY_AUTH_TOKEN`.

### Creating new environment

This project has been developed with Python 3.6 but it's has been tested with versions 2.7 and 3.4.

To create a new environment execute `python3 -m venv venv`. Make sure to config your _auth token_ in `venv/bin/activate` file. To activate run `source venv/bin/activate` and to deactivate run `source deactivate`.

### Tests

Running tests with _pytest_ it's pretty easy: `pytest tests`. You may check tests coverage with `pytest --cov=hunter/ tests` and the "flakes" (errors) with `flake8 hunter/`.
