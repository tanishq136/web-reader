import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from server.app.app import app
from server.app.webreader import WebAnswer, WebReaderError, extract_page_text


class FakeResponse:
    headers = {"content-type": "text/html; charset=utf-8"}
    text = "<html><body><h1>Example title</h1><script>ignored()</script><p>Useful page text.</p></body></html>"

    def raise_for_status(self):
        return None


class FakeSession:
    def get(self, *args, **kwargs):
        return FakeResponse()


class WebReaderTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_extract_page_text_removes_script_content(self):
        text = extract_page_text("https://example.com", session=FakeSession())
        self.assertEqual(text, "Example title Useful page text.")

    def test_health_endpoint(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    @patch("server.app.app.answer_question")
    def test_explain_returns_answer(self, answer_question):
        answer_question.return_value = WebAnswer("Example answer", 42)
        response = self.client.post("/explain", json={"url": "https://example.com", "query": "What is this?"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"output": "Example answer", "source_characters": 42})

    @patch("server.app.app.answer_question", side_effect=WebReaderError("Missing configuration", 503))
    def test_explain_returns_safe_service_error(self, _answer_question):
        response = self.client.post("/explain", json={"url": "https://example.com", "query": "What is this?"})
        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.json()["detail"], "Missing configuration")


if __name__ == "__main__":
    unittest.main()
