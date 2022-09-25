# Oauth2 Authorization Flow

Anything not mentioned in this guide in relation to Oauth2 is unused.

Oauth2 is a huge mess, don't expect for some standard or something.

## 1. App registration

You have to `POST` to `/oauth/apps/` with a Json body:

```json
{
    "name": "owo",
    "redirect_uris": "https://your/url/whatever",
    "scopes": "read write read:check_oauth_token read:app read:parts write:parts read:projects write:projects"
}
```

Notes:
- the `scopes` have to be thoses ones.

You will get in response:
```json
{
  "client_id": "xxx",
  "name": "xxx",
  "scopes": "xxx",
  "client_secret": "xxx",
  "created": "2022-09-25T19:38:34.134Z",
  "updated": "2022-09-25T19:38:34.134Z",
  "redirect_uris": "xxx"
}
```

You will most likely be interested in `client_id` and `client_secret`

## 2. Obtain token

You have to `POST` to `/oauth/token/` with a Json body:

```json
{
    "client_id": "xxx",
    "client_secret": "xxx",
    "grant_type": "password",
    "scope": "read write read:check_oauth_token read:app read:parts write:parts read:projects write:projects",
    "username": "xxx",
    "password": "xxx"
}
```

Notes:
- the `scopes` have to be thoses ones.
- only the grant `password` is supported

You will get in response:
```json
{
  "access_token": "xxx",
  "expires_in": 0,
  "token_type": "Bearer",
  "scope": "xxx",
  "refresh_token": "xxx"
}
```

You will most likely be interested in `access_token`.

## 3. Check token validity

You have to `GET` to `/oauth/check_token/`, with the right `Authorization` header.

You will get:

```json
{
  "token": "xxx",
  "expiry": "xxx",
  "valid": true,
  "user": {
    "username": "xxx"
  }
}
```

## 4. Profit

Do any call you want, just don't forget the `Authorization` header with content `Bearer ACCESS_TOKEN_HERE`.

## 5. Token revokation

You have to `POST` to `/oauth/revoke/` with a Json body:

```json
{
    "client_id": "xxx", 
    "client_secret": "xxx",
    "token": "xxx"
}
```

This call also needs to be authenticated with a header `Authorization: Bearer ACCESS_TOKEN`.

You will get a 200 without anything else.
