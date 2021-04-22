"""ETL for legacy Rose of Eternity reviews archived on wayback machine."""

import logging
from typing import Optional

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


def download_review(url: str) -> Optional[str]:
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


if __name__ == '__main__':
    for url in settings.URLS:
        review: Optional[str] = download_review(url)
