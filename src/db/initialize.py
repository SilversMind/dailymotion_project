import mysql
from constants import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE

def init_db():
    client = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD
        )
        
    cursor = client.cursor()
    database_name = MYSQL_DATABASE
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")

    # Step 4: Optionally, select the newly created database
    cursor.execute(f"USE {database_name}")

    # Create tables
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        email VARCHAR(255) UNIQUE NOT NULL,
        hashed_password VARCHAR(255) NOT NULL,
        activation_status TINYINT(1) NOT NULL DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)


    client.commit()
    cursor.close()
    client.close()