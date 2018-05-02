# Hashtag API
### API for an unbeatable tic-tac-toe minimax algorithm

[![Build Status](https://travis-ci.org/nateinaction/hashtag-api.svg?branch=master)](https://travis-ci.org/nateinaction/hashtag-api)
[![Maintainability](https://api.codeclimate.com/v1/badges/8b92aa472debf9d246f9/maintainability)](https://codeclimate.com/github/nateinaction/hashtag-api/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/8b92aa472debf9d246f9/test_coverage)](https://codeclimate.com/github/nateinaction/hashtag-api/test_coverage)

#### How to deploy

- Push to master automatically triggers TravisCI
- Heroku detects passing build from TravisCI and deploys

#### How to query API

- Send a POST request to the API endpoint:

```
curl -X POST \
  https://API_ENDPOINT_URL/ \
  -H 'Content-Type: application/json' \
  -d '{
	"board": [["x", "o", "x"], ["x", "o", "o"], ["o", "x", null]]
}'
```
