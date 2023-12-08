from typing import Tuple, List
from karrio.schemas.usps.carrier_pickup_schedule_request import (
    CarrierPickupScheduleRequest,
    PackageType,
)
from karrio.core.utils import Serializable, SF
from karrio.core.units import Packages
from karrio.core.models import (
    ShipmentRequest,
    PickupRequest,
    PickupDetails,
    Message,
)

from karrio.providers.usps.error import parse_error_response
from karrio.providers.usps.utils import Settings
import karrio.lib as lib


def parse_pickup_response(
    _response: lib.Deserializable[dict],
    settings: Settings,
) -> Tuple[PickupDetails, List[Message]]:
    response = _response.deserialize()
    errors = parse_error_response(response, settings)
    details = None

    return details, errors


def pickup_request(payload: PickupRequest, settings: Settings) -> Serializable:
    shipments: List[ShipmentRequest] = payload.options.get("shipments", [])
    packages = Packages(payload.parcels)

    request = CarrierPickupScheduleRequest(
        USERID=settings.username,
        FirstName=payload.address.person_name,
        LastName=None,
        FirmName=payload.address.company_name,
        SuiteOrApt=payload.address.address_line1,
        Address2=SF.concat_str(
            payload.address.address_line1, payload.address.address_line2, join=True
        ),
        Urbanization=None,
        City=payload.address.city,
        State=payload.address.state_code,
        ZIP5=payload.address.postal_code,
        ZIP4=None,
        Phone=payload.address.phone_number,
        Extension=None,
        Package=[
            PackageType(ServiceType=shipment.service, Count=len(shipment.parcels))
            for shipment in shipments
        ],
        EstimatedWeight=packages.weight.LB,
        PackageLocation=payload.package_location,
        SpecialInstructions=payload.instruction,
        EmailAddress=payload.address.email,
    )

    return Serializable(request)
