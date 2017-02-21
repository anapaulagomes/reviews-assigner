# Review's Hunter

Hunt some Udacity's revision automatically 🔦 [![Build Status](https://travis-ci.org/anapaulagomes/review-hunter.svg?branch=master)](https://travis-ci.org/anapaulagomes/review-hunter)

This project is focused on Udacity's reviewer. Considering this, you should have an _auth token_.
Add it as environment variable with the name __UDACITY_AUTH_TOKEN__.

### Creating new environment

`python3 -m venv venv`

Activating: `source venv/bin/activate`

Deactivating: `source deactivate`

### Tests

Running tests

`pytest tests`

Coverage

`pytest --cov=hunter/ tests`
