# -*- coding: utf-8 -*-
# pylint: disable=C0103

import json
from typing import Any, Dict, List
from flask import request

from delpinos.api.core.requests.api_request import ApiRequest


class FlaskRequest(ApiRequest):
    @property
    def method(self) -> str:
        return request.method

    @property
    def data(self) -> Dict[str, Any] | List[Dict[str, Any]]:
        try:
            if request.headers["Content-Type"] == "application/x-www-form-urlencoded":
                return self.form
            return self.body
        except Exception:
            return {}

    @property
    def body(self) -> Dict[str, Any] | List[Dict[str, Any]]:
        try:
            data = json.loads(request.get_data().decode("utf-8"))
            return data
        except Exception:
            return {}

    @property
    def query(self) -> Dict[str, Any]:
        try:
            data = dict(request.args)
            return data
        except Exception as e:
            print(e)
            return {}

    @property
    def form(self) -> Dict[str, Any]:
        try:
            data = dict(request.values)
            return data
        except Exception:
            return {}

    @property
    def headers(self) -> Dict[str, Any]:
        try:
            data = dict(request.headers)
            return data
        except Exception:
            return {}

    @property
    def cookies(self) -> Dict[str, Any]:
        try:
            data = dict(request.headers)
            return data
        except Exception:
            return {}

    def get_content(
        self,
        encoding: str = "utf-8",
        errors: str = "strict",
    ) -> str:
        try:
            return request.data.decode(encoding, errors)
        except Exception:
            return ""
