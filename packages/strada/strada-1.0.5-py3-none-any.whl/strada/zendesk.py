from .sdk import HttpRequestExecutor
from .exception_handler import exception_handler
from .common import (
    build_input_schema_from_strada_param_definitions,
)


class ZendeskCustomHttpActionBuilder:
    def __init__(self):
        self._instance = None

    def set_param_schema(self, param_schema):
        self._get_instance().param_schema_definition = (
            build_input_schema_from_strada_param_definitions(param_schema)
        )
        return self

    def set_url(self, url):
        self._get_instance().url = url
        return self

    def set_method(self, method):
        self._get_instance().method = method
        return self

    def set_token(self, access_token):
        self._get_instance().token = access_token
        return self

    def set_path(self, path):
        self._get_instance().path = path
        return self

    def set_headers(self, headers):
        self._instance.headers = headers
        return self

    def set_params(self, params):
        self._instance.params = params
        return self

    def set_body(self, body):
        self._instance.body = body
        return self

    def build(self):
        return self._get_instance()

    def _get_instance(self):
        if self._instance is None:
            self._instance = ZendeskCustomHttpAction()
        return self._instance


class ZendeskCustomHttpAction:
    def __init__(self):
        self.param_schema_definition = None
        self.url = None
        self.method = None
        self.token = None
        self.path = "{}"
        self.headers = "{}"
        self.params = "{}"
        self.body = "{}"

    @exception_handler
    def execute(self, **kwargs):
        return HttpRequestExecutor.execute(
            dynamic_parameter_json_schema=self.param_schema_definition,
            base_path_params=self.path,
            base_headers=self.headers,
            base_query_params=self.params,
            base_body=self.body,
            base_url=self.url,
            method=self.method,
            header_overrides={
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
            },
            **kwargs,
        )

    @staticmethod
    def prepare(data: dict):
        builder = ZendeskCustomHttpActionBuilder()
        return (
            builder.set_param_schema(data["param_schema_definition"])
            .set_url(data["url"])
            .set_method(data["method"])
            .set_token(data["access_token"])
            .set_headers(data.get("headers", "{}"))
            .set_path(data.get("path", "{}"))
            .set_params(data.get("params", "{}"))
            .set_body(data.get("body", "{}"))
            .build()
        )
