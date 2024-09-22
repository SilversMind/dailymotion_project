import os

# MySQL environment variable
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_PORT = os.getenv('MYSQL_PORT')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')
MYSQL_TEST_DATABASE="dm_test_db"
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')

# Redis environment variable
REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')

# Mailhog environment variable
MAILHOG_HOST = os.getenv('MAILHOG_HOST')
MAILHOG_PORT = os.getenv('MAILHOG_PORT')

# Misc
LOGGER_NAME = "Dailymotion WebApp Logger"

