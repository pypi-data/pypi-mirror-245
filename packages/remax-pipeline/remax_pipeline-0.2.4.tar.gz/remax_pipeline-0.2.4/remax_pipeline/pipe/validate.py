from ..models import HomeListing
from ..utils.logging import logger


class Validate:
    @staticmethod
    def catch(func, handle=lambda e: e, *args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.warning(f"Contract failed:{e}")
            return None

    @staticmethod
    def data_contract(extracted_data: list):
        return [data for data in [Validate.catch(lambda: HomeListing(**data)) for data in extracted_data] if data]
