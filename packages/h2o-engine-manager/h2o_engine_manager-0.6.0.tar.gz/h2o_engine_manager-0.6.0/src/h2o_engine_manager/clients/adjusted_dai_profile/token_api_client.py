from typing import Callable

from h2o_engine_manager.gen import api_client


class TokenApiClient(api_client.ApiClient):
    """Overrides update_params_for_auth method of the generated ApiClient classes"""

    def __init__(
            self, configuration: api_client.Configuration, token_provider: Callable[[], str]
    ):
        self._token_provider = token_provider
        super().__init__(configuration=configuration)

    def update_params_for_auth(
            self,
            headers,
            queries,
            auth_settings,
            resource_path,
            method,
            body,
            request_auths=None,
    ):
        token = self._token_provider()
        headers["Authorization"] = f"Bearer {token}"
