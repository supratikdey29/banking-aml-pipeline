from datetime import datetime
import uuid


# ==========================================================
# STANDARD EVENT ENVELOPE
# ==========================================================
def add_event_metadata(

    payload: dict,

    event_type="INSERT",

    source_system="CORE_BANKING",

    schema_version="1.0"

):

    payload["event_id"] = str(uuid.uuid4())

    payload["event_type"] = event_type

    payload["event_timestamp"] = datetime.utcnow().strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )

    payload["source_system"] = source_system

    payload["schema_version"] = schema_version

    return payload