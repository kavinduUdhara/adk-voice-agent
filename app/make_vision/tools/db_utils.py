"""
Utility functions for connecting to and querying the Cloud SQL PostgreSQL database.
"""

import os
from dotenv import load_dotenv
from google.cloud.sql.connector import Connector
import pg8000

# Load environment variables from .env
load_dotenv()

# Global connector for reuse
_connector = Connector()

# Required database config from environment
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")
DB_INSTANCE = os.getenv("DB_INSTANCE")


def get_connection():
    """
    Establish a secure connection to the Cloud SQL PostgreSQL instance using the Cloud SQL connector.

    Returns:
        A pg8000 connection object
    """
    print("Connecting to database")
    return _connector.connect(
        DB_INSTANCE,
        "pg8000",
        user=DB_USER,
        password=DB_PASS,
        db=DB_NAME,
    )


def run_query(query: str, params: tuple = ()):
    """
    Execute a SQL query and return all rows.

    Args:
        query (str): SQL query string with placeholders (e.g., "SELECT * FROM users WHERE id = %s")
        params (tuple): Tuple of parameters to substitute into the query

    Returns:
        list: List of result rows
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


def run_query_single(query: str, params: tuple = ()):
    """
    Execute a SQL query and return a single row.

    Args:
        query (str): SQL query string
        params (tuple): Query parameters

    Returns:
        tuple or None: A single row, or None if no result
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()


def run_non_query(query: str, params: tuple = ()):
    """
    Execute an INSERT, UPDATE, or DELETE statement.

    Args:
        query (str): SQL command
        params (tuple): Parameters for the command

    Returns:
        int: Number of affected rows
    """
    conn = get_connection()
    print(conn)
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        conn.commit()
        return cursor.rowcount
    finally:
        cursor.close()
        conn.close()
