"""Unit tests."""

import pytest

from etl.etl import download_review

@pytest.mark.parametrize('response_mock', [
    {'text': 'response', 'status_code': 200},
    {'text': None, 'status_code': 404},
])
def test_download_review(requests_mock, response_mock):
    fake_url = 'http://fake_url.com'
    requests_mock.get(fake_url, status_code=response_mock['status_code'], text=response_mock['text'])
    assert response_mock['text'] == download_review(fake_url)
