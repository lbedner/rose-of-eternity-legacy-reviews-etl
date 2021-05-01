"""Unit tests."""

import os
from unittest.mock import patch, mock_open

import pytest

from etl.etl import (
    download_review_page,
    scrape_review_page,
    write_reviews_to_tsv,
)
from etl import settings

REVIEW_PAGE_GOOD = """
<body>
	<center>
		<table>>
			<tr class="fmsalt2">
				<td class="fmsalt2">
					<a href="View.php?view=User.Profile&amp;id=27320" target="_new">pokstair</a>
				</td>
				<td class="fmsalt2">10.00</td>
				<td class="fmsalt2">Review 2</td>
				<td class="fmsalt2">10-13-2006</td>
			</tr>
			<tr class="fmsalt1">
				<td class="fmsalt1">
					<a href="View.php?view=User.Profile&amp;id=90838" target="_new">RapidDeployment</a>
				</td>
				<td class="fmsalt1">10.00</td>
				<td class="fmsalt1">Review 1</td>
				<td class="fmsalt1">10-12-2006</td>
			</tr>
		</table>
"""

REVIEWS = [
    {
        'user_id': '90838',
        'user_name': 'RapidDeployment',
        'score': '10.00',
        'content': 'Review 1',
        'date': '2006-10-12',
    },
    {
        'user_id': '27320',
        'user_name': 'pokstair',
        'score': '10.00',
        'content': 'Review 2',
        'date': '2006-10-13',
    },
]

@pytest.mark.parametrize('response_mock', [
    {'text': 'response', 'status_code': 200},
    {'text': None, 'status_code': 404},
])
def test_download_review(requests_mock, response_mock):
    fake_url: str = 'http://fake_url.com'
    requests_mock.get(fake_url, status_code=response_mock['status_code'], text=response_mock['text'])
    assert response_mock['text'] == download_review_page(fake_url)


def test_scrape_review_page():
    reviews: list[dict] = scrape_review_page(REVIEW_PAGE_GOOD)
    assert reviews
    assert len(reviews) == 2
    assert reviews[0] == REVIEWS[0]
    assert reviews[1] == REVIEWS[1]


@patch("builtins.open", new_callable=mock_open())
def test_write_reviews_to_tsv(mock_open):
    tsv_filename = write_reviews_to_tsv('foo.html', REVIEWS)
    assert tsv_filename == os.path.join(settings.REVIEWS_OUTPUT_FOLDER, 'foo.tsv')
