from io import BytesIO
import base64
import requests
from .sdk import HttpRequestExecutor, StradaResponse, StradaError
from .exception_handler import exception_handler
from .common import (
    build_input_schema_from_strada_param_definitions,
    hydrate_input_fields,
    validate_http_input,
)


class OpenAICustomHttpActionBuilder:
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

    def set_headers(self, headers):
        self._instance.headers = headers
        return self

    def set_path_params(self, path_params):
        self._instance.path = path_params
        return self

    def set_query_params(self, params):
        self._instance.params = params
        return self

    def set_body(self, body):
        self._instance.body = body
        return self

    def build(self):
        return self._get_instance()

    def _get_instance(self):
        if self._instance is None:
            self._instance = OpenAICustomHttpAction()
        return self._instance


class OpenAICustomHttpAction:
    def __init__(self):
        self.param_schema_definition = None
        self.url = None
        self.method = None
        self.token = None
        self.headers = "{}"
        self.path = "{}"
        self.params = "{}"
        self.body = "{}"
    
    def _execute_with_file(self, **kwargs):
        validate_http_input(self.param_schema_definition, **kwargs)

        headers = hydrate_input_fields(
            self.param_schema_definition, self.headers, **kwargs
        )
        query_params = hydrate_input_fields(
            self.param_schema_definition, self.params, **kwargs
        )
        body = hydrate_input_fields(self.param_schema_definition, self.body, **kwargs)

        headers["Authorization"] = f"Bearer {self.token}"

        base_64_file_str = body.get("file", None)
        if base_64_file_str is None:
            return StradaResponse(
                success=False,
                error=StradaError(
                    errorCode=400,
                    statusCode=400,
                    message="No 'file' provided.'file' is required."
                )
            )
        MIME_type = body.get("MIME_type", None)
        if MIME_type is None:
            return StradaResponse(
                success=False,
                error=StradaError(
                    errorCode=400,
                    statusCode=400,
                    message="No 'MIME_type' provided. 'MIME_type' is required."
                )
            )

        base_64_decoded = base64.b64decode(base_64_file_str)
        del body["file"]
        del body["MIME_type"]

        response = requests.request(
            self.method, self.url, headers=headers, params=query_params, data=body,
            files={'file': ('input_file', BytesIO(base_64_decoded), MIME_type)}
        )

        response_data = response.json()
        if response.ok:  # HTTP status code 200-299
            return StradaResponse(success=True, data=response_data)
        else:
            # If the response contains structured error information, you can parse it here
            error_message = response_data.get("message", None)
            if error_message is None:
                error_message = response_data.get("error", None)
            if error_message is None:
                error_message = response.text
            if error_message is None:
                error_message = "Error executing HTTP Request."

            error = StradaError(
                errorCode=response.status_code,
                statusCode=response.status_code,
                message=error_message,
            )
            return StradaResponse(success=False, data=response_data, error=error)


    @exception_handler
    def execute(self, **kwargs):
        if 'audio/transcriptions' or 'audio/translations' in self.url:
            return self._execute_with_file(**kwargs)
        else:
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
    def prepare(data):
        builder = OpenAICustomHttpActionBuilder()
        return (
            builder.set_param_schema(data["param_schema_definition"])
            .set_url(data["url"])
            .set_method(data["method"])
            .set_token(data["access_token"])
            .set_path_params(data.get("path", "{}"))
            .set_headers(data.get("headers", "{}"))
            .set_query_params(data.get("query", "{}"))
            .set_body(data.get("body", "{}"))
            .build()
        )