"""Configuration settings."""

from decouple import config, Csv

URLS = config('URLS', cast=Csv())

REVIEWS_OUTPUT_FOLDER = config(
    'REVIEWS_OUTPUT_FOLDER',
    default='./output/reviews',
)

LOG_FILE = config('LOG_FILE', default=None)
LOG_LEVEL = config('LOG_LEVEL', default='INFO')
