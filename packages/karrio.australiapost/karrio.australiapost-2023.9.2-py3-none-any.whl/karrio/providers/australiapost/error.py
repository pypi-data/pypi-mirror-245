from typing import List
from karrio.schemas.australiapost.error import Error
from karrio.core.models import Message
from karrio.providers.australiapost import Settings


def parse_error_response(response: dict, settings: Settings) -> List[Message]:
    errors: List[dict] = response.get("errors", [])
    return [_extract_error(Error(**e), settings) for e in errors]


def _extract_error(error: Error, settings: Settings) -> Message:
    return Message(
        # context info
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        # carrier error info
        code=(error.error_code or error.code),
        message=error.message,
        details=dict(
            name=(error.error_name or error.name),
            field=error.field,
            context=error.context,
        ),
    )
