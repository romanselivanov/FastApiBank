from os import environ
from core.config import settings
import databases

TESTING = environ.get("TESTING")

if TESTING:
    # Use separate DB for tests
    DB_NAME = "test-bank-temp-for-test"
    TEST_SQLALCHEMY_DATABASE_URL = (settings.TEST_SQLALCHEMY_DATABASE_URI)
    database = databases.Database(TEST_SQLALCHEMY_DATABASE_URL)
else:
    DB_NAME = "test-bank"
    SQLALCHEMY_DATABASE_URL = (settings.SQLALCHEMY_DATABASE_URI)
    database = databases.Database(SQLALCHEMY_DATABASE_URL)
