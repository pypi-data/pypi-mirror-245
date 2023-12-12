import json
from urllib.error import HTTPError
from urllib.request import Request, build_opener

from django.conf import settings


class PowCaptchaValidationException(Exception):
    pass


def powcaptcha_request(path, params):
    domain = getattr(settings, 'POWCAPTCHA_API_URL')
    token = getattr(settings, 'POWCAPTCHA_API_TOKEN')

    request_object = Request(
        url=f'https://{domain}/{path}',
        data=params,
        headers={
            'Authorization': f'Bearer {token}',
        },
    )

    opener_args = []
    opener = build_opener(*opener_args)

    return opener.open(
        request_object,
        timeout=5
    )


def get_challenge():
    path = 'GetChallenges?difficultyLevel=5'
    response = powcaptcha_request(path, [])
    challenges = json.loads(response.read().decode('utf-8'))

    # @Todo: implement caching

    return challenges[0]


def validate_captcha(challenge: str, nonce: str):
    path = f'Verify?challenge={challenge}&nonce={nonce}'

    try:
        powcaptcha_request(path, [])
    except HTTPError as error:
        raise PowCaptchaValidationException(error.code)
