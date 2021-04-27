"""ETL for legacy Rose of Eternity reviews archived on wayback machine."""

import csv
from dateutil import parser
import logging
import os
from typing import Optional

from bs4 import BeautifulSoup
import requests

from . import settings

# Setup logger
if settings.LOG_FILE:
    logging.basicConfig(filename=settings.LOG_FILE, filemode='w')
formatter: logging.Formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s',
)
logger: logging.Logger = logging.getLogger(__name__)
handler: logging.StreamHandler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(settings.LOG_LEVEL)


def download_review_page(url: str) -> Optional[str]:
    """Download and returns a HTML page representing the review.

    Args:
        url: Wayback machine URL.

    Returns:
        HTML page representing the review.
    """
    logger.info(f'Downloading: {url}')

    response: requests.Response = requests.get(url)
    response_code: int = response.status_code
    if response_code == 200:
        logger.info(f'Success - Response Code {response_code}')
        return response.text
    logger.info(f'Failure - Response Code {response_code}')
    return None


def scrape_review_page(review_page: str) -> list[dict]:
    """Scrape the review page and return all the reviews.

    Args:
        review_page: HTML representation of the review.

    Returns:
        Reviews.
    """
    reviews: list[dict] = []

    soup: BeautifulSoup = BeautifulSoup(review_page, 'html.parser')
    table: BeautifulSoup = soup.body.center.table
    rows: list = table.find_all('tr')

    for row in rows:
        columns: list = row.find_all('td')
        if columns:

            # User Data
            user_data_column: BeautifulSoup = columns[0]
            user_id = user_data_column.a.attrs['href'].split('id')[1].replace(
                '=',
                ''
            )
            user_name = user_data_column.find('a', href=True).text

            # Review Score
            review_score: float = columns[1].text

            # Review
            content: str = columns[2].text

            # Review Date
            review_date: str = parser.parse(
                columns[3].text
            ).strftime('%Y-%m-%d')

            review = {
                'user_id': user_id,
                'user_name': user_name,
                'score': review_score,
                'content': content,
                'date': review_date,
            }
            reviews.append(review)

    logger.info(f'Scraped {len(reviews)} Reviews!')

    # Reverse list so that the reviews at the bottom of the page
    # (which are the earliest) are at the beginning of the list
    reviews.reverse()
    return reviews


def write_reviews_to_csv(url: str, reviews: list[dict]) -> Optional[str]:
    """Write reviews to CSV file.

    Args:
        url: Wayback machine URL.
        reviews: Scaped reviews.

    Returns:
        Name of CSV file.
    """
    # Create CSV filename based off of Wayback Machine URL
    # and output directory
    csv_filename: str = os.path.basename(url).replace('html', 'csv')
    csv_filename = os.path.join(settings.REVIEWS_OUTPUT_FOLDER, csv_filename)

    # Write CSV file
    logger.info(f'Writing {csv_filename}')
    with open(csv_filename, 'w', newline='') as output_file:
        dict_writer: csv.DictWriter = csv.DictWriter(
            output_file,
            fieldnames=reviews[0].keys(),
        )
        dict_writer.writeheader()
        dict_writer.writerows(reviews)
        return csv_filename
    return None


if __name__ == '__main__':

    for url in settings.URLS:

        # Download and store reviews (HTML)
        review_page: Optional[str] = download_review_page(url)

        # Scrape the review page for reviews
        if review_page:
            reviews: list[dict] = scrape_review_page(review_page)

            # Export reviews to CSV file
            csv_filename: Optional[str] = write_reviews_to_csv(url, reviews)
