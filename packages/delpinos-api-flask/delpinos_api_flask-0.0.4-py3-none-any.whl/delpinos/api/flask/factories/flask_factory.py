import os
from flask import Flask
from delpinos.api.core.factories.api_factory import ApiFactory
from delpinos.api.flask.controllers.flask_controller import FlaskController
from delpinos.api.flask.requests.flask_request import FlaskRequest
from delpinos.api.flask.responses.flask_response import FlaskResponse


class FlaskFactory(ApiFactory):
    @property
    def app(self) -> Flask:
        return self.instance("api.app", Flask)

    def add_factories(self):
        self.add_factory("api.app", lambda _: Flask("__main__"))
        super().add_factories()

    def add_factories_controllers(self):
        self.add_factory_impl("api.controllers.api_controller", FlaskController)

    def add_factories_encoders(self):
        super().add_factories_encoders()

    def add_factories_requests(self):
        self.add_factory_impl("api.requests.api_request", FlaskRequest)

    def add_factories_responses(self):
        self.add_factory_impl("api.responses.api_response", FlaskResponse)

    def server(self):
        port = int(os.getenv("PORT", "5000"))
        self.app.run(debug=self.debug, host="0.0.0.0", port=port)
