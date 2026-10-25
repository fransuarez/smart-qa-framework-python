import unittest
from unittest.mock import patch, MagicMock
from utils.api_client import APIClient

class TestAPIClient(unittest.TestCase):
    @patch('utils.api_client.requests.Session')
    def test_get_success(self, mock_session):
        mock_resp = MagicMock()
        mock_resp.json.return_value = {"key": "value"}
        mock_resp.status_code = 200
        mock_resp.raise_for_status.return_value = None
        mock_session.return_value.request.return_value = mock_resp

        client = APIClient(
            base_url="https://example.com",
            token_url="/auth",
            username="u",
            password="p"
        )
        result = client.get("/some-endpoint")
        self.assertEqual(result, {"key": "value"})
        mock_session.return_value.request.assert_called_with(
            "get", "https://example.com/some-endpoint", params=None
        )

    @patch('utils.api_client.requests.Session')
    def test_get_failure(self, mock_session):
        mock_resp = MagicMock()
        mock_resp.json.return_value = {"key": "value"}
        mock_resp.status_code = 401
        mock_resp.raise_for_status.return_value = None
        mock_session.return_value.request.return_value = mock_resp

        client = APIClient(
            base_url="https://example.com",
            token_url="/auth",
            username="u",
            password="p"
        )
        with self.assertRaises(requests.HTTPError):
            client.get("/some-endpoint")
        mock_session.return_value.request.assert_called_with(
            "get", "https://example.com/some-endpoint", params=None
        )

    @patch('utils.api_client.requests.Session')
    def test_post_success(self, mock_session):
        mock_resp = MagicMock()
        mock_resp.json.return_value = {"key": "value"}
        mock_resp.status_code = 200
        mock_resp.raise_for_status.return_value = None
        mock_session.return_value.request.return_value = mock_resp

        client = APIClient(
            base_url="https://example.com",
            token_url="/auth",
            username="u",
            password="p"
        )
        result = client.post("/some-endpoint", json={"key": "value"})
        self.assertEqual(result, {"key": "value"})
        mock_session.return_value.request.assert_called_with(
            "post", "https://example.com/some-endpoint", json={"key": "value"}
        )

    @patch('utils.api_client.requests.Session')
    def test_post_failure(self, mock_session):
        mock_resp = MagicMock()
        mock_resp.json.return_value = {"key": "value"}
        mock_resp.status_code = 401
        mock_resp.raise_for_status.return_value = None
        mock_session.return_value.request.return_value = mock_resp

        client = APIClient(
            base_url="https://example.com",
            token_url="/auth",
            username="u",
            password="p"
        )
        with self.assertRaises(requests.HTTPError):
            client.post("/some-endpoint", json={"key": "value"})
        mock_session.return_value.request.assert_called_with(
            "post", "https://example.com/some-endpoint", json={"key": "value"}
        )

if __name__ == "__main__":
    unittest.main()