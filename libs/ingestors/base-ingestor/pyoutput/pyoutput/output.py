import traceback
from pystatus import client_error
import base64
import json
from datetime import datetime

def new_bad_request_error_status(error):
    return {
        "code": client_error.BAD_REQUEST,
        "detail": _get_error_details(error)
    }


def _get_error_details(error):
    return "Error: {} Traceback: {}".format(error, traceback.format_exc())


def new_metadata(input_msg, processing_id=None):
    input_ = input_msg
    if isinstance(input_msg, dict):
        input_id = input_msg.get("_id")
        input_ = {
            "fields": base64.b64encode(json.dumps(input_msg).encode()).decode()
        }
        if input_id is not None:
            input_.update({
                "_id": input_id
            })
    metadata = {
        "input": input_,
        "processingTimestamp": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    }
    return _add_processing_id(metadata, input_msg, processing_id)


def _add_processing_id(metadata, input_msg, processing_id):
    processing_id_key = "processingId"
    if isinstance(input_msg, dict) and input_msg.get(processing_id_key):
        metadata[processing_id_key] = input_msg[processing_id_key]
        return metadata
    if processing_id is not None:
        metadata[processing_id_key] = processing_id
    return metadata


def new_unhandled_error_status(input_msg):
    ...


def new_status():
    ...


def new_no_output_produced_error_status():
    ...
