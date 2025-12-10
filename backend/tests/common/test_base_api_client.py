import httpx
import pytest
import pytest_asyncio
import respx

from src.common.base_api_client import BaseAPIClient
from src.common.exceptions import ExternalServiceException


@pytest.fixture
def mock_base_url():
    return "https://example.com/api"


@pytest.fixture
def mock_endpoint():
    return "/test-endpoint"


@pytest_asyncio.fixture
async def api_client():
    async with httpx.AsyncClient() as client:
        yield client


@pytest.fixture
def base_client(api_client, mock_base_url):
    return BaseAPIClient(base_url=mock_base_url, client=api_client)


class TestBaseAPIClient:
    @respx.mock
    @pytest.mark.asyncio
    async def test_get_success(self, base_client, mock_base_url, mock_endpoint):
        # Arrange
        expected_response = {"key": "value"}
        respx.get(f"{mock_base_url}{mock_endpoint}").mock(
            return_value=httpx.Response(200, json=expected_response)
        )

        # Act
        response = await base_client.get(mock_endpoint)

        # Assert
        assert response == expected_response

    @respx.mock
    @pytest.mark.asyncio
    async def test_get_timeout(self, base_client, mock_base_url, mock_endpoint):
        # Arrange
        respx.get(f"{mock_base_url}{mock_endpoint}").mock(
            side_effect=httpx.TimeoutException("Request timed out")
        )

        # Act & Assert
        with pytest.raises(ExternalServiceException) as exc_info:
            await base_client.get(mock_endpoint)

        assert "timed out" in str(exc_info.value)

    @respx.mock
    @pytest.mark.asyncio
    async def test_get_http_error(self, base_client, mock_base_url, mock_endpoint):
        # Arrange
        respx.get(f"{mock_base_url}{mock_endpoint}").mock(
            return_value=httpx.Response(404, json={"message": "Not Found"})
        )

        # Act & Assert
        with pytest.raises(ExternalServiceException) as exc_info:
            await base_client.get(mock_endpoint)

        assert "404" in str(exc_info.value)

    @respx.mock
    @pytest.mark.asyncio
    async def test_get_network_error(self, base_client, mock_base_url, mock_endpoint):
        # Arrange
        respx.get(f"{mock_base_url}{mock_endpoint}").mock(
            side_effect=httpx.RequestError("Connection refused")
        )

        # Act & Assert
        with pytest.raises(ExternalServiceException) as exc_info:
            await base_client.get(mock_endpoint)

        assert "Failed to connect" in str(exc_info.value)

    @respx.mock
    @pytest.mark.asyncio
    async def test_get_invalid_json(self, base_client, mock_base_url, mock_endpoint):
        # Arrange
        respx.get(f"{mock_base_url}{mock_endpoint}").mock(
            return_value=httpx.Response(500, text="Internal Server Error")
        )

        # Act & Assert
        with pytest.raises(ExternalServiceException) as exc_info:
            await base_client.get(mock_endpoint)

        assert "500" in str(exc_info.value)
