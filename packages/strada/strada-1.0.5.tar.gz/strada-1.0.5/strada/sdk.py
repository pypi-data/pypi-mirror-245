from typing import Any
from pydantic import BaseModel
import requests
from .common import (
    hydrate_input_fields,
    validate_http_input,
    fill_path_params,
)

class StradaError(BaseModel):
    errorCode: int
    statusCode: int
    message: str


class StradaResponse(BaseModel):
    error: StradaError = None
    success: bool
    data: Any = None


class HttpRequestExecutor:
    @staticmethod
    def execute(
        dynamic_parameter_json_schema: dict,
        base_path_params,
        base_headers,
        base_query_params,
        base_body,
        base_url: str,
        method: str,
        header_overrides: dict = {},
        **kwargs
    ) -> StradaResponse:
        validate_http_input(dynamic_parameter_json_schema, **kwargs)

        path_params = hydrate_input_fields(
            dynamic_parameter_json_schema, base_path_params, **kwargs
        )
        headers = hydrate_input_fields(
            dynamic_parameter_json_schema, base_headers, **kwargs
        )
        query_params = hydrate_input_fields(
            dynamic_parameter_json_schema, base_query_params, **kwargs
        )
        body = hydrate_input_fields(dynamic_parameter_json_schema, base_body, **kwargs)

        for key, value in header_overrides.items():
            headers[key] = value

        url = fill_path_params(base_url, path_params)

        if (
            headers.get("Content-Type") == "application/json"
            or headers.get("content-type") == "application/json"
        ):
            response = requests.request(
                method, url, headers=headers, params=query_params, json=body
            )
        else:
            response = requests.request(
                method, url, headers=headers, params=query_params, data=body
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
