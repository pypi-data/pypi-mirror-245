import requests

from sklik.exception import SklikException
from sklik.util import SKLIK_API_URL


def _handle_response(response: requests.Response) -> dict[str, any]:
    response_content = response.json()
    if response_content['status'] != 200:
        raise SklikException(
            msg=f"Could not request {response.url}: status code {response_content.get('status')}",
            status_code=response_content.get('status'),
            additional_information=response_content.get('statusMessage')
        )
    return response_content


def sklik_request(api_url: str, service: str, method: str, args: str | list) -> dict[str, any]:
    """
    Perform a request to the Sklik API.

    :param api_url: The base URL of the Sklik API.
    :type api_url: str
    :param service: The service name to be called in the API.
    :type service: str
    :param method: The method name to be called in the API.
    :type method: str
    :param args: The arguments to be passed in the request. It can be a string or a list.
    :type args: str | list
    :return: The response from the Sklik API as a dictionary.
    :rtype: dict[str, any]
    """
    request_url = f'{api_url}/{service}.{method}'
    response = requests.post(url=request_url, json=args)
    return _handle_response(response)


class SklikApi:
    """
    Sklik API class for interacting with the Sklik advertising platform.

    Attributes:
        _default_api: The default instance of the SklikApi class.

    Args:
        session (str): The session token for authentication.

    Methods:
        __init__(self, session: str) -> None:
            Initializes a new instance of the SklikApi class with the given session token.

        init(cls, token: str) -> SklikApi:
            Static method to create a new SklikApi instance and set it as the default API.

        set_default_api(cls, api: SklikApi) -> None:
            Static method to set the default API instance.

        get_default_api(cls) -> SklikApi:
            Static method to get the default API instance.

        _update_session(self, response) -> None:
            Internal method to update the session token.

        _preprocess_call(self, args: list | None) -> list[dict[str, any]]:
            Internal method to preprocess the API call args and add the session token.

        call(self, service: str, method: str, args: list | None = None) -> dict[str, any]:
            Makes a Sklik API call with the specified service, method, and args.

    """
    _default_api = None

    def __init__(self, session: str):
        self.session = session

    @classmethod
    def init(cls, token: str) -> 'SklikApi':
        response = sklik_request(SKLIK_API_URL, 'client', 'loginByToken', args=token)
        api = cls(response['session'])
        cls.set_default_api(api)
        return api

    @classmethod
    def set_default_api(cls, api: 'SklikApi') -> None:
        cls._default_api = api

    @classmethod
    def get_default_api(cls) -> 'SklikApi':
        return cls._default_api

    def _update_session(self, response) -> None:
        self.session = response['session']

    def _preprocess_call(self, args: list | None) -> list[dict[str, any]]:
        session_args = [{'session': self.session}]
        if not args:
            return session_args

        if isinstance(args[0], dict) and args[0].get('userId'):
            args[0]['session'] = self.session
        else:
            args = session_args + args
        return args

    def call(self, service: str, method: str, args: list | None = None) -> dict[str, any]:
        """
        Calls the specified service method with the given arguments and returns the response.

        :param service: The name of the service to call.
        :param method: The name of the method to call.
        :param args: The arguments to pass to the method. This parameter is optional.
        :type args: list[str] or None
        :return: The response from the service method call.
        :rtype: dict[str, any]
        """
        payload = self._preprocess_call(args)
        response = sklik_request(SKLIK_API_URL, service, method, payload)
        self._update_session(response)
        return response
