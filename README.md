# Review's Hunter

Hunt some Udacity's revision automatically 🔦 [![Build Status](https://travis-ci.org/anapaulagomes/review-hunter.svg?branch=master)](https://travis-ci.org/anapaulagomes/review-hunter)

## How it works

This project is focused on Udacity's reviewer. Considering this, you should have an _auth token_.
Add it as environment variable with the name __UDACITY_AUTH_TOKEN__.

## Development

I've tried to develop this with TDD. So take a look on tests to follow the hunter's logic.

### Tech Stack

- Python 3
- requests
- py.test

### Creating new environment

```
python3 -m venv venv
```

Activating
```
source venv/bin/activate
```

Deactivating
```
deactivate
```

### Tests

Running tests

```
py.test hunter
```
