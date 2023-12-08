import karrio.schemas.dpdhl.business_interface as dpdhl
import time
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.dpdhl.error as error
import karrio.providers.dpdhl.utils as provider_utils
import karrio.providers.dpdhl.units as provider_units


def parse_shipment_response(
    _response: lib.Deserializable[lib.Element],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    response = _response.deserialize()
    response_shipment: typing.Optional[dpdhl.CreationState] = lib.find_element(
        "CreationState",
        response,
        dpdhl.CreationState,
        first=True,
    )

    messages = error.parse_error_response(response, settings)
    shipment = (
        _extract_details(response_shipment, settings)
        if getattr(response_shipment, "shipmentNumber", None) is not None
        else None
    )

    return shipment, messages


def _extract_details(
    shipment: dpdhl.CreationState,
    settings: provider_utils.Settings,
) -> models.ShipmentDetails:
    label = shipment.LabelData.labelData

    return models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=shipment.shipmentNumber,
        shipment_identifier=shipment.shipmentNumber,
        label_type="PDF",
        docs=models.Documents(label=label),
        meta=dict(
            carrier_tracking_link=settings.tracking_url.format(shipment.shipmentNumber),
        ),
    )


def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    customs = lib.to_customs_info(payload.customs)
    packages = lib.to_packages(payload.parcels)
    service = provider_units.ShippingService.map(payload.service).value_or_key
    label_type = provider_units.LabelType.map(payload.label_type or "PDF").value
    options = lib.to_shipping_options(
        payload.options,
        initializer=provider_units.shipping_options_initializer,
    )

    account_number = provider_units.ServicePrefix.account_suffix(
        settings.account_number,
        service=service,
        options=options,
        settings=settings,
        is_international=shipper.country_code != recipient.country_code,
    )
    return_account_number = (
        provider_units.ServicePrefix.account_suffix(
            options.return_account_number.state,
            service=service,
            options=options,
            settings=settings,
            is_international=shipper.country_code != recipient.country_code,
        )
        if options.return_account_number.state is not None
        else account_number
    )

    request = lib.Envelope(
        Header=lib.Header(
            provider_utils.AuthentificationType(
                user=("2222222222_01" if settings.test_mode else settings.username),
                signature=("pass" if settings.test_mode else settings.password),
            ),
        ),
        Body=lib.Body(
            dpdhl.CreateShipmentOrderRequest(
                Version=dpdhl.Version(
                    majorRelease=3,
                    minorRelease=4,
                ),
                ShipmentOrder=[
                    dpdhl.ShipmentOrderType(
                        sequenceNumber=index,
                        Shipment=dpdhl.ShipmentType(
                            ShipmentDetails=dpdhl.ShipmentDetailsTypeType(
                                product=service,
                                accountNumber=account_number,
                                customerReference=None,
                                shipmentDate=(
                                    options.shipment_date.state
                                    or time.strftime("%Y-%m-%d")
                                ),
                                costCentre=(settings.metadata or {}).get(
                                    "cost-reference"
                                ),
                                returnShipmentAccountNumber=return_account_number,
                                returnShipmentReference=None,
                                ShipmentItem=dpdhl.ShipmentItemType(
                                    weightInKG=package.weight.KG,
                                    lengthInCM=package.length.CM,
                                    widthInCM=package.width.CM,
                                    heightInCM=package.height.CM,
                                ),
                                Service=(
                                    dpdhl.ShipmentService(
                                        IndividualSenderRequirement=(
                                            int(
                                                options.dpdhl_individual_sender_requirement.state
                                            )
                                            if "dpdhl_individual_sender_requirement"
                                            in options
                                            else None
                                        ),
                                        PackagingReturn=(
                                            int(options.dpdhl_packaging_return.state)
                                            if "dpdhl_packaging_return" in options
                                            else None
                                        ),
                                        Endorsement=(
                                            int(options.dpdhl_endorsement.state)
                                            if "dpdhl_endorsement" in options
                                            else None
                                        ),
                                        VisualCheckOfAge=(
                                            int(options.dpdhl_visual_check_of_age.state)
                                            if "dpdhl_visual_check_of_age" in options
                                            else None
                                        ),
                                        PreferredLocation=options.dpdhl_preferred_location.state,
                                        PreferredNeighbour=options.dpdhl_preferred_neighbour.state,
                                        PreferredDay=options.dpdhl_preferred_day.state,
                                        NoNeighbourDelivery=(
                                            int(
                                                options.dpdhl_no_neighbour_delivery.state
                                            )
                                            if "dpdhl_no_neighbour_delivery" in options
                                            else None
                                        ),
                                        NamedPersonOnly=(
                                            int(options.dpdhl_named_person_only.state)
                                            if "dpdhl_named_person_only" in options
                                            else None
                                        ),
                                        ReturnReceipt=(
                                            int(options.dpdhl_return_receipt.state)
                                            if "dpdhl_return_receipt" in options
                                            else None
                                        ),
                                        Premium=(
                                            int(options.dpdhl_premium.state)
                                            if "dpdhl_premium" in options
                                            else None
                                        ),
                                        CashOnDelivery=options.dpdhl_cash_on_delivery.state,
                                        PDDP=(
                                            int(
                                                getattr(customs.duty, "incoterm", None)
                                                == "DDP"
                                            )
                                            if customs.is_defined
                                            else None
                                        ),
                                        AdditionalInsurance=options.dpdhl_additional_insurance.state,
                                        BulkyGoods=(
                                            int(options.dpdhl_bulky_goods.state)
                                            if "dpdhl_bulky_goods" in options
                                            else None
                                        ),
                                        IdentCheck=(
                                            dpdhl.IdentType(
                                                surname=options.dpdhl_identcheck.state.get(
                                                    "surname"
                                                ),
                                                givenName=options.dpdhl_identcheck.state.get(
                                                    "givenName"
                                                ),
                                                dateOfBirth=options.dpdhl_identcheck.state.get(
                                                    "dateOfBirth"
                                                ),
                                                minimumAge=options.dpdhl_identcheck.state.get(
                                                    "minimumAge"
                                                ),
                                            )
                                            if "dpdhl_identcheck" in options
                                            else None
                                        ),
                                        ParcelOutletRouting=options.email_notification_to.state,
                                    )
                                    if any(options.items())
                                    else None
                                ),
                                Notification=(
                                    dpdhl.ShipmentNotificationType(
                                        recipientEmailAddress=(
                                            options.email_notification_to.state
                                            or recipient.email
                                        )
                                    )
                                    if options.email_notification.state
                                    else None
                                ),
                                BankData=None,
                            ),
                            Shipper=dpdhl.ShipperType(
                                Name=dpdhl.NameType(
                                    name1=shipper.address_line1,
                                    name2=shipper.address_line2,
                                    name3=None,
                                ),
                                Address=dpdhl.NativeAddressTypeNew(
                                    streetName=shipper.street_name,
                                    streetNumber=shipper.street_number,
                                    addressAddition=None,
                                    dispatchingInformation=None,
                                    zip=dpdhl.ZipType(shipper.postal_code),
                                    city=shipper.city,
                                    province=shipper.state_code,
                                    Origin=dpdhl.CountryType(
                                        country=shipper.country_name,
                                        countryISOCode=shipper.country_code,
                                    ),
                                ),
                                Communication=(
                                    dpdhl.CommunicationType(
                                        phone=shipper.phone_number,
                                        email=shipper.email,
                                        contactPerson=shipper.person_name,
                                    )
                                    if shipper.has_contact_info
                                    else None
                                ),
                            ),
                            ShipperReference=payload.reference,
                            Receiver=dpdhl.ReceiverType(
                                name1=recipient.address_line1,
                                Address=dpdhl.ReceiverNativeAddressType(
                                    name2=(
                                        options.dpdhl_packstation.state
                                        or recipient.address_line2
                                    ),
                                    name3=None,
                                    streetName=(
                                        recipient.street_name
                                        if (options.dpdhl_packstation.state is None)
                                        else "Packstation"
                                    ),
                                    streetNumber=recipient.street_number,
                                    addressAddition=None,
                                    dispatchingInformation=None,
                                    zip=dpdhl.ZipType(recipient.postal_code),
                                    city=recipient.city,
                                    province=recipient.state_code,
                                    Origin=dpdhl.CountryType(
                                        country=recipient.country_name,
                                        countryISOCode=recipient.country_code,
                                    ),
                                ),
                                Packstation=None,
                                Postfiliale=None,
                                Communication=(
                                    dpdhl.CommunicationType(
                                        phone=recipient.phone_number,
                                        email=recipient.email,
                                        contactPerson=(
                                            recipient.person_name
                                            or recipient.company_name
                                        ),
                                    )
                                    if recipient.has_contact_info
                                    else None
                                ),
                            ),
                            ReturnReceiver=None,
                            ExportDocument=(
                                dpdhl.ExportDocumentType(
                                    invoiceNumber=customs.invoice,
                                    exportType=provider_units.CustomsContentType.map(
                                        customs.content_type or "other"
                                    ).value,
                                    exportTypeDescription=(
                                        customs.content_description
                                        or provider_units.CustomsContentType.map(
                                            customs.content_type or "other"
                                        ).value
                                    ),
                                    termsOfTrade=provider_units.Incoterm.map(
                                        customs.incoterm
                                    ).value,
                                    placeOfCommital=shipper.country_name,
                                    additionalFee=None,
                                    customsCurrency=(
                                        getattr(customs.duty, "currency", None)
                                        or options.currency.state
                                    ),
                                    permitNumber=customs.options.permit_number.state,
                                    attestationNumber=customs.options.attestation_number.state,
                                    addresseesCustomsReference=None,
                                    sendersCustomsReference=None,
                                    WithElectronicExportNtfctn=None,
                                    ExportDocPosition=[
                                        dpdhl.ExportDocPositionType(
                                            description=lib.text(
                                                item.title
                                                or item.description
                                                or "N/A"
                                                or item.sku,
                                                max=35,
                                            ),
                                            countryCodeOrigin=(
                                                item.origin_country
                                                or shipper.country_code
                                            ),
                                            customsTariffNumber=(
                                                item.hs_code or item.sku
                                            ),
                                            amount=(item.quantity or 1),
                                            netWeightInKG=units.Weight(
                                                item.weight, item.weight_unit or "KG"
                                            ).KG,
                                            customsValue=(item.value_amount or 1.0),
                                        )
                                        for item in customs.commodities
                                    ],
                                )
                                if customs.is_defined
                                else None
                            ),
                            feederSystem=None,
                        ),
                        PrintOnlyIfCodeable=None,
                    )
                    for index, package in enumerate(packages, start=1)
                ],
                labelResponseType=label_type,
                groupProfileName=None,
                labelFormat=None,
                labelFormatRetoure=None,
                combinedPrinting="0",
            ),
        ),
    )

    return lib.Serializable(
        request,
        lambda envelope: lib.envelope_serializer(
            envelope,
            namespace=(
                'xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"'
                ' xmlns:cis="http://dhl.de/webservice/cisbase"'
                ' xmlns:ns="http://dhl.de/webservices/businesscustomershipping/3.0"'
            ),
            prefixes=dict(
                name1="cis",
                ShipmentOrder="",
                Envelope="soapenv",
                Version_children="",
                Name_children="cis",
                accountNumber="cis",
                combinedPrinting="",
                labelResponseType="",
                Address_children="cis",
                AuthentificationType="cis",
                Communication_children="cis",
                CreateShipmentOrderRequest="ns",
            ),
        ),
    )
