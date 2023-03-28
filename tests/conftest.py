import pytest
import requests
from tests.test_config import API_URL
import logging

logging.basicConfig(level=logging.INFO)


@pytest.fixture()
def api_client():
    base_url = API_URL
    headers = {"Content-Type": "application/json"}

    def _send_request(method, endpoint=None, **kwargs):
        url = base_url if endpoint is None else f"{base_url}/{endpoint}"
        logging.info(
            f"Making {method} request to {url} with body: {kwargs.get('json')}")
        response = requests.request(method, url, headers=headers, **kwargs)
        logging.debug(
            f"Received response with status code: {response.status_code}, body: {response.content}")
        return response

    yield _send_request


@pytest.fixture
def check_successful_response():
    def _check_successful_response(response):
        assert response.status_code == 200 or response.status_code == 201
        assert len(response.json()) > 0
        assert response.json()["status"] == "success"
    return _check_successful_response


@pytest.fixture
def check_error_response():
    def _check_error_response(response, status_code):
        assert response.status_code == status_code
        assert len(response.json()) > 0
        assert response.json()["status"] == "error"
    return _check_error_response
