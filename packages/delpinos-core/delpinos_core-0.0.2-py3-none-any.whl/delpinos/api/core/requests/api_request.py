# -*- coding: utf-8 -*-
# pylint: disable=C0103,C0114,C0115,C0116,W0718

import base64
from delpinos.core.factories.factory import Factory
from delpinos.api.core.requests.api_request_abstract import (
    Any,
    Dict,
    List,
    ApiRequestAbstract,
)


class ApiRequest(ApiRequestAbstract, Factory):
    def method(self) -> str:
        raise NotImplementedError()

    @property
    def data(self) -> Dict[str, Any] | List[Dict[str, Any]]:
        raise NotImplementedError()

    @property
    def body(self) -> Dict[str, Any]:
        raise NotImplementedError()

    @property
    def query(self) -> Dict[str, Any]:
        raise NotImplementedError()

    @property
    def form(self) -> Dict[str, Any]:
        raise NotImplementedError()

    @property
    def headers(self) -> Dict[str, Any]:
        raise NotImplementedError()

    @property
    def cookies(self) -> Dict[str, Any]:
        raise NotImplementedError()

    @property
    def files(self) -> Dict[str, Any]:
        raise NotImplementedError()

    def get_content(
        self,
        encoding: str = "utf-8",
        errors: str = "strict",
    ) -> str:
        raise NotImplementedError()

    def get_authorization(self, token_type=None, token: str | None = None) -> str:
        try:
            if token:
                return str(token).rsplit(" ", maxsplit=1)[-1].strip()
            token = self.headers.get("Authorization") or ""
            parts = str(token).strip().split(" ")
            if parts[0].lower() != token_type:
                return ""
            return parts[-1].strip()
        except Exception as err:
            # self.logger.error(err)
            return ""

    def get_basic_authorization(self) -> Dict[str, Any]:
        try:
            basic_authorization = self.get_authorization("basic") or ""
            user, password = (
                base64.b64decode(basic_authorization.encode("utf-8"))
                .decode("utf-8")
                .split(":")
            )
        except Exception:
            user = None
            password = None
        return {"user": user, "password": password}
