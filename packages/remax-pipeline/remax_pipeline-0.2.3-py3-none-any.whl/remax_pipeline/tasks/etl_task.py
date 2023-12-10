import time

from ..pipe import Extract, Load, Validate


def start_task(pages: list):
    worker_start_time = time.time()
    return Load.push_to_db(
        Validate.data_contract(Extract.get_listing_data(pages=pages, multithreaded=True)), worker_start_time
    )
