import httpx
import logging
from typing import Optional, Dict, Any, Union

from app.utils.logs import get_logger

logger = get_logger(__name__)

class ApiClient:
    def __init__(self, base_url: str, default_headers: Optional[Dict[str, str]] = None):
        self.base_url = base_url.rstrip('/')
        self.default_headers = default_headers or {}

    async def send_request(self, endpoint: str, method: str, body: Optional[Dict[str, Any]] = None,
                        form_data: Optional[Dict[str, Any]] = None,
                        headers: Optional[Dict[str, str]] = None) -> Union[Dict[str, Any], str]:

        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        request_headers = {**self.default_headers, "Content-Type": "application/json"}

        if headers:
            request_headers.update(headers)

        try:
            async with httpx.AsyncClient() as client:
                if form_data:
                    request_headers["Content-Type"] = "application/x-www-form-urlencoded"
                    response = await client.request(method, url, data=form_data, headers=request_headers)
                else:
                    response = await client.request(method, url, json=body, headers=request_headers)

                if not response.is_success:
                    return self.handle_error(response)

                return response.json()
        except httpx.RequestError as exc:
            logger.error(f"Request error for {url}: {exc}")
            raise RuntimeError(f"Request error: {exc}") from exc


    def handle_error(self, response: httpx.Response):
        status = response.status_code
        text = response.text
        logger.error(f"Request failed with status code {status}, URL: {response.url}, Response: {text}")

        if status == 400:
            raise ValueError(f"Bad Request: {text}")
        elif status == 401:
            raise PermissionError("Unauthorized")
        elif status == 403:
            raise PermissionError("Forbidden")
        elif status == 404:
            raise FileNotFoundError(f"Not Found: {text}")
        elif status == 409:
            raise ValueError(f"Conflict: {text}")
        elif status == 413:
            raise ValueError("Payload Too Large")
        elif status == 500:
            raise RuntimeError("Server Error")
        else:
            raise RuntimeError(f"Unhandled Error {status}: {text}")

    async def get(self, endpoint: str, body: Optional[Dict[str, Any]] = None,
                  headers: Optional[Dict[str, str]] = None) -> Union[Dict[str, Any], str]:
        return await self.send_request(endpoint, "GET", body=body, headers=headers)

    async def post(self, endpoint: str, body: Optional[Dict[str, Any]] = None, 
                   form_data: Optional[Dict[str, Any]] = None,
                   headers: Optional[Dict[str, str]] = None) -> Union[Dict[str, Any], str]:
        return await self.send_request(endpoint, "POST", body=body, form_data=form_data, headers=headers)

    async def put(self, endpoint: str, body: Dict[str, Any],
                  headers: Optional[Dict[str, str]] = None) -> Union[Dict[str, Any], str]:
        return await self.send_request(endpoint, "PUT", body, None, headers)

    async def delete(self, endpoint: str,
                     headers: Optional[Dict[str, str]] = None) -> Union[Dict[str, Any], str]:
        return await self.send_request(endpoint, "DELETE", None, None, headers)
