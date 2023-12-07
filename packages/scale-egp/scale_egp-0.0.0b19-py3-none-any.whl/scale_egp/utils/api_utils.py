import functools
import json
from typing import (
    Any,
    List,
    Optional,
    TYPE_CHECKING,
    Dict,
    Iterable,
    Callable,
)
from urllib.parse import urljoin

from httpx import Response

from scale_egp.exceptions import exception_from_response
from scale_egp.utils.model_utils import BaseModel

if TYPE_CHECKING:
    from scale_egp.sdk.client import EGPClient

DEFAULT_TIMEOUT = 60


def handle_api_exceptions(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)
        if response.status_code != 200:
            raise exception_from_response(response)
        return response

    return wrapper


class APIEngine:
    def __init__(self, api_client: "EGPClient"):
        self._api_client = api_client

    def _post(
        self,
        sub_path: str,
        request: Optional[BaseModel] = None,
        timeout: Optional[int] = None,
    ) -> Response:
        response = self._raw_post(
            sub_path=sub_path,
            request_json=request.model_dump() if request is not None else None,
            timeout=timeout if timeout is not None else DEFAULT_TIMEOUT,
        )
        return response

    def _post_stream(
        self,
        sub_path: str,
        request: Optional[BaseModel] = None,
        timeout: Optional[int] = None,
    ) -> Iterable[Dict[str, Any]]:
        response = self._raw_stream(
            sub_path=sub_path,
            request_json=request.model_dump() if request is not None else None,
            timeout=timeout if timeout is not None else DEFAULT_TIMEOUT,
        )
        with response as lines:
            for line in lines.iter_lines():
                if line.startswith('data: '):
                    event_json_str = line[len('data: '):]
                    try:
                        yield json.loads(event_json_str)
                    except json.JSONDecodeError:
                        raise ValueError(f"Invalid JSON payload: {event_json_str}")

    def _post_batch(
        self,
        sub_path: str,
        request_batch: Optional[List[BaseModel]] = None,
        timeout: Optional[int] = None,
    ) -> Response:
        response = self._raw_post(
            sub_path=sub_path,
            request_json=[request.model_dump() for request in request_batch],
            timeout=timeout if timeout is not None else DEFAULT_TIMEOUT,
        )
        return response

    def _get(
        self,
        sub_path: str,
        query_params: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
    ) -> Response:
        response = self._raw_get(
            sub_path=sub_path,
            query_params=query_params,
            timeout=timeout if timeout is not None else DEFAULT_TIMEOUT,
        )
        return response

    def _patch(
        self,
        sub_path: str,
        request: Optional[BaseModel] = None,
        timeout: Optional[int] = None,
    ) -> Response:
        response = self._raw_patch(
            sub_path=sub_path,
            request_json=request.model_dump() if request is not None else None,
            timeout=timeout if timeout is not None else DEFAULT_TIMEOUT,
        )
        return response

    def _delete(
        self,
        sub_path: str,
        timeout: Optional[int] = None,
    ) -> Response:
        response = self._raw_delete(
            sub_path=sub_path,
            timeout=timeout if timeout is not None else DEFAULT_TIMEOUT,
        )
        return response

    @handle_api_exceptions
    def _raw_post(
        self,
        sub_path: str,
        request_json: Optional[Dict[str, Any]] = None,
        timeout: Optional[int] = None,
        additional_headers: Optional[Dict[str, str]] = None,
    ) -> Response:
        response = self._api_client.httpx_client.post(
            urljoin(self._api_client.endpoint_url, sub_path),
            json=request_json,
            **self._universal_request_kwargs(
                timeout=timeout,
                additional_headers=additional_headers,
            ),
        )
        return response

    def _raw_stream(
        self,
        sub_path: str,
        request_json: Optional[Dict[str, Any]] = None,
        timeout: Optional[int] = None,
        additional_headers: Optional[Dict[str, str]] = None,
        method: str = "POST",
    ):
        return self._api_client.httpx_client.stream(
            method=method,
            url=urljoin(self._api_client.endpoint_url, sub_path),
            json=request_json,
            timeout=timeout if timeout is not None else DEFAULT_TIMEOUT,
            headers={
                **(additional_headers if additional_headers is not None else {}),
            },
        )

    @handle_api_exceptions
    def _raw_get(
        self,
        sub_path: str,
        timeout: Optional[int] = None,
        query_params: Optional[Dict[str, str]] = None,
        additional_headers: Optional[Dict[str, str]] = None,
    ) -> Response:
        response = self._api_client.httpx_client.get(
            urljoin(self._api_client.endpoint_url, sub_path),
            params=query_params,
            **self._universal_request_kwargs(
                timeout=timeout,
                additional_headers=additional_headers,
            ),
        )
        return response

    @handle_api_exceptions
    def _raw_patch(
        self,
        sub_path: str,
        request_json: Optional[Dict[str, Any]] = None,
        timeout: Optional[int] = None,
        additional_headers: Optional[Dict[str, str]] = None,
    ) -> Response:
        response = self._api_client.httpx_client.patch(
            urljoin(self._api_client.endpoint_url, sub_path),
            json=request_json,
            **self._universal_request_kwargs(
                timeout=timeout,
                additional_headers=additional_headers,
            ),
        )
        return response

    @handle_api_exceptions
    def _raw_delete(
        self,
        sub_path: str,
        timeout: Optional[int] = None,
        additional_headers: Optional[Dict[str, str]] = None,
    ) -> Response:
        response = self._api_client.httpx_client.delete(
            url=urljoin(self._api_client.endpoint_url, sub_path),
            **self._universal_request_kwargs(
                timeout=timeout,
                additional_headers=additional_headers,
            ),
        )
        return response

    def _universal_request_kwargs(
        self,
        timeout: Optional[int] = None,
        additional_headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        return dict(
            timeout=timeout if timeout is not None else DEFAULT_TIMEOUT,
            headers={
                **(additional_headers if additional_headers is not None else {}),
            },
        )
