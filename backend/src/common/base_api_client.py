import httpx

from src.common.exceptions import ExternalServiceException


class BaseAPIClient:
    service_name = None

    def __init__(self, base_url: str, client: httpx.AsyncClient):
        self.base_url = base_url
        self.client = client

    async def get(self, endpoint: str, params: dict = {}) -> dict:
        url = self.base_url + endpoint

        try:
            response = await self.client.get(url, params=params, timeout=10.0)
            response.raise_for_status()
            return response.json()

        except httpx.TimeoutException as e:
            raise ExternalServiceException(
                f"{self.service_name} API request timed out: {str(e)}"
            ) from e

        except httpx.HTTPStatusError as e:
            error_detail = "Unknown error"
            try:
                error_data = e.response.json()
                error_detail = error_data.get("message", str(e))
            except Exception:
                error_detail = e.response.text or str(e)

            raise ExternalServiceException(
                f"{self.service_name} API returned error (status {e.response.status_code}): {error_detail}"
            ) from e

        except httpx.RequestError as e:
            raise ExternalServiceException(
                f"Failed to connect to {self.service_name} API: {str(e)}"
            ) from e

        except Exception as e:
            raise ExternalServiceException(
                f"Unexpected error calling {self.service_name} API: {str(e)}"
            ) from e
