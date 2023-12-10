import time
from typing import List

from ..models import HomeListing
from ..services.sql_service import insert_listings


class Load:
    @staticmethod
    def push_to_db(listings: List[HomeListing], start_time: float) -> dict:
        response = insert_listings(listings)
        response["time(s)"] = time.time() - start_time
        return response
