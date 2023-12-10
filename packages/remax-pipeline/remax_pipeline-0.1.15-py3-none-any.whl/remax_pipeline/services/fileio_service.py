import json
import os
from pathlib import Path

from bson import ObjectId

from remax_pipeline.utils.logging import logger


class CustomEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return super().default(o)


def read_json(filename: str):
    path = Path(f"{os.getcwd()}/temp") / filename
    with open(path, "r") as file:
        data = json.load(file)
    return data


def write_to_json_local(result, filename: str):

    path = Path(f"{os.getcwd()}/temp") / filename
    json_str = json.dumps(result, cls=CustomEncoder)

    with path.open("w") as json_file:
        logger.debug("writing to local file")
        json_file.write(json_str)
