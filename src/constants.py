import os

# MySQL environment variable
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')
MYSQL_TEST_DATABASE=os.getenv('MYSQL_TEST_DATABASE', "dm_test_db")
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')

# Redis environment variable
REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')

# Misc
LOGGER_NAME = "Dailymotion WebApp Logger"

