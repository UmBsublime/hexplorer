class ApiUnauthorizedError(Exception):
    ...


class ApiFailledToGetResponse(Exception):
    ...


class ApiRateLimitExceededError(Exception):
    ...


class ApiBadRequestError(Exception):
    ...


class ApiResourceNotFoundError(Exception):
    ...
