import uuid
from datetime import date


def generate_uuid_from_string(input_string: str):
    namespace_uuid = uuid.NAMESPACE_DNS  # Use the DNS namespace UUID
    generated_uuid = uuid.uuid5(namespace_uuid, input_string)
    return str(generated_uuid)


def generate_listing_primary_key(input_string: str):
    namespace_uuid = uuid.NAMESPACE_DNS  # Use the DNS namespace UUID
    generated_uuid = uuid.uuid5(namespace_uuid, input_string + str(date.today()))
    return str(generated_uuid)
