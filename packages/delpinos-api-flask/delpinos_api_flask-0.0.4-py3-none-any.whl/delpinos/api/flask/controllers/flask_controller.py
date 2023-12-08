# -*- coding: utf-8 -*-
# pylint: disable=C0103

from typing import Callable, List

from flask import Flask
from flask import send_file
from flask import Response as FlaskResponse
from delpinos.api.core.controllers.api_controller import ApiController

from delpinos.api.core.responses.api_response_abstract import ApiResponseAbstract


class FlaskController(ApiController):
    @property
    def app(self) -> Flask:
        return self.instance("api.app", Flask)

    def add_endpoint(
        self,
        endpoint: str,
        callback: Callable[..., ApiResponseAbstract],
        methods: List[str] = [],
    ) -> "FlaskController":
        def view_func(*args, **kwargs) -> FlaskResponse:
            response: ApiResponseAbstract = callback(*args, **kwargs)
            if response.fmt == "file":
                return send_file(
                    response.response,
                    mimetype=response.mimetype,
                    as_attachment=bool(response.get("as_attachment")),
                    download_name=response.get("download_name"),
                    conditional=bool(response.get("conditional")),
                    etag=bool(response.get("etag")),
                    last_modified=response.get("last_modified"),
                    max_age=response.get("max_age"),
                )
            return FlaskResponse(
                response=response.response,
                status=response.status,
                headers=response.headers,
                mimetype=response.mimetype,
                content_type=response.content_type,
            )

        self.app.add_url_rule(
            rule=endpoint, endpoint=endpoint, view_func=view_func, methods=methods
        )
        return self
