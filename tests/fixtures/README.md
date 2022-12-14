# Fixtures

- [`v2_2xx_responses.json`](v2_2xx_responses.json) was initially generated from
  [CompanyCam v2.postman_collection.json](../../openapi-spec/CompanyCam%20v2.postman_collection.json)
  (as at companycam/openapi-spec@7dd5ab1).
  - Converted using `transform_postman_collection()` (see [helpers.py](helpers.py)).
  - `{{baseUrl}}/companies/:id` was changed to `{{baseUrl}}/company` to reflect the
    [OpenAPI specification](../../openapi-spec/openapi.yaml).
  - Added data for the following paths since they were missing:
    - `GET /projects/{}/assigned_users` – copied from `GET /users`
    - `PUT /projects/{}/assigned_users/{}` – copied from `PUT /users/{}`
    - `DELETE /projects/{}/assigned_users/{}`
    - `GET /projects/{}/collaborators` – created from real API call, but no data to work with, so it's only an empty list
    - `GET /projects/{}/comments` – created from real API call
    - `POST /projects/{}/comments` – created from real API call
    - `GET /projects/{}/invitations` – created from real API calls
    - `POST /projects/{}/invitations` – created from real API call
    - `PUT /projects/{}/notepad` – created from real API call
    - `GET /users/{}` – copied from `PUT /users/{}`
