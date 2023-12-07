from requests import Session

from redstat.variables.application import APPLICATION_AUTHOR, APPLICATION_NAME, APPLICATION_VERSION

BASE_HEADER = {
    'user-agent': f'{APPLICATION_NAME} {APPLICATION_VERSION} {APPLICATION_AUTHOR}'
}

SESSION = Session()
SESSION.headers.update(BASE_HEADER)
