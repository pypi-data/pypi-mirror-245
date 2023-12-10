import sys
import time

import psycopg2
from psycopg2 import sql

from ..config.settings import PostegresSettings
from ..utils.logging import logger

TIMEOUT = 1000

settings = PostegresSettings()


def database_exists(conn, dbname):
    """Check if a database exists."""
    with conn.cursor() as cursor:
        cursor.execute(sql.SQL("Select 1 FROM pg_database WHERE datname = %s;"), (dbname,))
        return cursor.fetchone() is not None


def create_database(conn, dbname):
    """Create a new database"""
    with conn.cursor() as cursor:
        cursor.execute(sql.SQL("CREATE DATABASE{}").format(sql.Identifier(dbname)))


def create_tables(conn):
    """Create home listing table"""

    query = sql.SQL(
        """
    CREATE TABLE IF NOT EXISTS {} (
        id UUID PRIMARY KEY,
        address_id UUID,
        full_address VARCHAR(255),
        street_name VARCHAR(255),
        city VARCHAR(255),
        province VARCHAR(255),
        postal_code VARCHAR(10),
        lat DOUBLE PRECISION,
        lon DOUBLE PRECISION,
        home_price DOUBLE PRECISION,
        bed INTEGER,
        bath INTEGER,
        property_type VARCHAR(20),
        description TEXT,
        listing_date DATE
    );
    """
    ).format(sql.Identifier("home_listings"))

    with conn.cursor() as cursor:
        try:
            cursor.execute(query)
        except Exception as e:
            logger.warning(e)


def connect():
    conn = psycopg2.connect(
        dbname=settings.dbname,
        user=settings.user,
        password=settings.password,
        host=settings.host,
        port=settings.port,
    )
    return conn


def initialize_database():

    start = time.time()
    logger.info(settings)

    while True:
        try:
            conn = connect()
            conn.autocommit = True
            logger.task("Connected to database")
            break
        except psycopg2.OperationalError as e:
            logger.warning(e)
            logger.debug("Postgres not available yet.. sleeping")
            time.sleep(1)

            if time.time() - start > TIMEOUT:
                logger.warning("Exiting...")
                sys.exit(-1)

    db_name = settings.dbname

    try:
        if not database_exists(conn, db_name):
            logger.debug(f"Database '{db_name}' does not exist! Will create it.")
            create_database(conn, db_name)
            logger.task(f"Created '{db_name}'!")
        else:
            logger.info(f"Database '{db_name}' already exists.")
        create_tables(conn)
    finally:
        conn.close()
    return
