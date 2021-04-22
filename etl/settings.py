"""Configuration settings."""

from decouple import config, Csv

URLS = config('URLS', cast=Csv())

LOG_FILE = config('LOG_FILE', default=None)
LOG_LEVEL = config('LOG_LEVEL', default='INFO')
