from typing import Dict, List

from psycopg2 import IntegrityError, extras, sql

from ..db import connect_db
from ..models import HomeListing
from ..utils.logging import logger


def scd():
    pass


@connect_db
def insert_listings(listings: List[HomeListing], conn=None):

    success, failure = 0, 0
    with conn.cursor() as cursor:
        for listing in listings:
            query = sql.SQL(
                """
            INSERT INTO {}
            (id, address_id, full_address, street_name, city, province, postal_code, lat, lon, home_price, bed, bath, property_type, description, listing_date)
            VALUES
            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """
            ).format(sql.Identifier("home_listings"))

            data = (
                listing.id,
                listing.address_id,
                listing.full_address,
                listing.street_name,
                listing.city,
                listing.province,
                listing.postal_code,
                listing.lat,
                listing.lon,
                listing.home_price,
                listing.bed,
                listing.bath,
                listing.property_type,
                listing.description,
                listing.listing_date,
            )

            try:
                cursor.execute(query, data)
                success += 1
            except IntegrityError as e:
                logger.warning(f"IntegrityError: {e}")
                failure += 1

    return {"success": success, "failure": failure, "success_rate": success / (success + failure)}


def insert_run_log():
    pass


@connect_db
def select_all_listings(conn=None) -> List[Dict]:
    with conn.cursor(cursor_factory=extras.DictCursor) as cursor:
        query = sql.SQL("SELECT * FROM {}").format(sql.Identifier("home_listings"))
        cursor.execute(query)
        result = [dict(row) for row in cursor.fetchall()]
    return result
