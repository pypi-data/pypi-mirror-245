# -*- coding: utf-8 -*-
# pylint: disable=C0103

from delpinos.api.core.requests.api_request import (
    Factory,
    ApiRequest,
    ApiRequestAbstract,
    Any,
    Dict,
    List,
)


class Request(ApiRequest):
    @property
    def impl(self) -> ApiRequestAbstract:
        return self.instance("api.requests.api_request", ApiRequestAbstract)

    @classmethod
    def add_factories_requests(cls, factory: Factory):
        factory.add_factory_impl("api.requests.api_request", ApiRequest)

    @property
    def method(self) -> str:
        return self.impl.method

    @property
    def data(self) -> Dict[str, Any] | List[Dict[str, Any]]:
        return self.impl.data

    @property
    def body(self) -> Dict[str, Any]:
        return self.impl.body

    @property
    def query(self) -> Dict[str, Any]:
        return self.impl.query

    @property
    def form(self) -> Dict[str, Any]:
        return self.impl.form

    @property
    def headers(self) -> Dict[str, Any]:
        return self.impl.headers

    @property
    def cookies(self) -> Dict[str, Any]:
        return self.impl.cookies

    @property
    def files(self) -> Dict[str, Any]:
        return self.impl.files

    def get_content(
        self,
        encoding: str = "utf-8",
        errors: str = "strict",
    ) -> str:
        return self.impl.get_content(encoding, errors)

    def get_authorization(self, token_type=None, token: str | None = None) -> str:
        return self.impl.get_authorization(token_type, token)

    def get_basic_authorization(self) -> Dict[str, Any]:
        return self.impl.get_basic_authorization()
