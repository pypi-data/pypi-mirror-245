from pydantic import BaseModel
from pydantic.alias_generators import to_camel
from sklik.api import SklikApi
from sklik.exception import SklikException


class AccountModel(BaseModel):
    class Config:
        title = 'client'
        alias_generator = to_camel
        populate_by_name = True

    user_id: int
    username: str
    wallet_credit: int | None
    wallet_credit_with_vat: int | None
    wallet_verified: bool | None
    day_budget_sum: int | None
    account_limit: int | None


class Account:
    """
    Account

    Class representing a Sklik account.

    Attributes:
        account_id (int): The ID of the account.
        api (SklikApi | None): The Sklik API object. Defaults to None.
        _model (AccountModel): The model object representing the account.

    Methods:
        __init__(self, account_id: int, api: SklikApi | None = None)
            Initializes an Account object.

        __getattr__(self, item)
            Retrieves an attribute of the Account object or the underlying model object.

        _build_model(self) -> AccountModel
            Builds the model object based on account data fetched from the API.

        _find_account_data(self, response: dict) -> dict | None
            Finds the account data within the API response.

        call(self, service: str, method: str, args: list) -> dict[str, any]
            Makes a call to the Sklik API with the specified service, method, and arguments.
    """
    def __init__(self, account_id: int, api: SklikApi | None = None):
        self.account_id = account_id
        self.api = api or SklikApi.get_default_api()
        self._model = self._build_model()

    def __getattr__(self, item):
        if hasattr(self, item):
            return getattr(self, item)
        if hasattr(self._model, item):
            return getattr(self._model, item)
        else:
            raise AttributeError(
                f"{self.__class__.__name__} nor {self._model.__class__.__name__} object has no attribute '{item}'")

    def _build_model(self) -> AccountModel:
        response = self.api.call('client', 'get')
        account_data = self._find_account_data(response)
        if not account_data:
            raise SklikException(
                msg=f"Unable to fetch account data from the API.",
                status_code=404,
                additional_information=None
            )
        return AccountModel.model_validate(account_data)

    def _find_account_data(self, response: dict) -> dict | None:
        if response['user']['userId'] == self.account_id:
            return response['user']
        for foreign_account in response['foreignAccounts']:
            if foreign_account['userId'] == self.account_id:
                return foreign_account
        return None

    def call(self, service: str, method: str, args: list) -> dict[str, any]:
        payload = [{'userId': self._model.user_id}] + args
        return self.api.call(service, method, payload)
