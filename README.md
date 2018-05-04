# Hashtag API
### API for an unbeatable tic-tac-toe minimax algorithm

[![Build Status](https://travis-ci.org/nateinaction/hashtag-api.svg?branch=master)](https://travis-ci.org/nateinaction/hashtag-api)
[![Maintainability](https://api.codeclimate.com/v1/badges/8b92aa472debf9d246f9/maintainability)](https://codeclimate.com/github/nateinaction/hashtag-api/maintainability)
[![codecov](https://codecov.io/gh/nateinaction/hashtag-api/branch/master/graph/badge.svg)](https://codecov.io/gh/nateinaction/hashtag-api)

#### How to deploy

- Push to master automatically triggers TravisCI
- Heroku detects passing build from TravisCI and deploys

#### How to query API

- Send a POST request to the API endpoint:

```bash
curl -X POST \
  https://API_ENDPOINT_URL/ \
  -H 'Content-Type: application/json' \
  -d '{
	"board": [["x", "o", "o"], [null, "x", null], [null, null, null]]
}'
```

### Types of responses

**State: playing**

```json
{
    "status": "playable",
    "playableToken": "x",
    "suggestedMove": {
        "col": 2,
        "row": 2
    }
}
```

**State: tied**

```json
{
    "status": "tied",
    "playableToken": null,
    "suggestedMove": null
}
```

**State: won**

```json
{
    "status": "won",
    "playableToken": "x",
    "suggestedMove": null
}
```
