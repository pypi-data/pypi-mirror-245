from typing import Tuple, List
from karrio.schemas.usps.evsi_cancel_request import eVSICancelRequest
from karrio.schemas.usps.evsi_cancel_response import eVSICancelResponse
from karrio.core.utils import Serializable, XP
from karrio.core.models import ShipmentCancelRequest, ConfirmationDetails, Message

from karrio.providers.usps_international.error import parse_error_response
from karrio.providers.usps_international.utils import Settings
import karrio.lib as lib


def parse_shipment_cancel_response(
    _response: lib.Deserializable[lib.Element],
    settings: Settings,
) -> Tuple[ConfirmationDetails, List[Message]]:
    response = _response.deserialize()
    errors: List[Message] = parse_error_response(response, settings)
    cancel_response = XP.to_object(eVSICancelResponse, response)

    if cancel_response.Status != "Cancelled":
        errors.append(
            Message(
                carrier_name=settings.carrier_name,
                carrier_id=settings.carrier_id,
                message=cancel_response.Reason,
                code=cancel_response.Status,
            )
        )

    details = (
        ConfirmationDetails(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            operation="Shipment Cancel",
            success=True,
        )
        if not any(errors)
        else None
    )

    return details, errors


def shipment_cancel_request(
    payload: ShipmentCancelRequest, settings: Settings
) -> Serializable:
    request = eVSICancelRequest(
        USERID=settings.username, BarcodeNumber=payload.shipment_identifier
    )

    return Serializable(request, XP.export)
