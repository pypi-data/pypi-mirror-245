from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import Client
from ...models.http_validation_error import HTTPValidationError
from ...models.process_information import ProcessInformation
from ...models.put_item_process_item_id_process_information_put_response_put_item_process_item_id_processinformation_put import (
    PutItemProcessItemIdProcessInformationPutResponsePutItemProcessItemIdProcessinformationPut,
)
from ...types import Response


def _get_kwargs(
    item_id: str,
    *,
    client: Client,
    json_body: ProcessInformation,
) -> Dict[str, Any]:
    url = "{}/Process/{item_id}/ProcessInformation/".format(client.base_url, item_id=item_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    return {
        "method": "put",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "json": json_json_body,
    }


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Optional[
    Union[
        Any,
        HTTPValidationError,
        PutItemProcessItemIdProcessInformationPutResponsePutItemProcessItemIdProcessinformationPut,
    ]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = (
            PutItemProcessItemIdProcessInformationPutResponsePutItemProcessItemIdProcessinformationPut.from_dict(
                response.json()
            )
        )

        return response_200
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = cast(Any, None)
        return response_404
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[
    Union[
        Any,
        HTTPValidationError,
        PutItemProcessItemIdProcessInformationPutResponsePutItemProcessItemIdProcessinformationPut,
    ]
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    item_id: str,
    *,
    client: Client,
    json_body: ProcessInformation,
) -> Response[
    Union[
        Any,
        HTTPValidationError,
        PutItemProcessItemIdProcessInformationPutResponsePutItemProcessItemIdProcessinformationPut,
    ]
]:
    """Put Item

    Args:
        item_id (str):
        json_body (ProcessInformation): The SubmodelElementCollection GeneralInfo contains 4
            SubmodelElements that allow to describe one specific process attribute in a structured,
            self-describing and interoperable way.
            The types are defined by DIN 8580 for Manufacturing Processes, VDI 2411 for Material Flow
            Processes, VDI 2243 for Remanufacturing Processes and VDI 2860 for Assembly.

            Args:
                id_ (str): The id of the general info.
                description (Optional[str]): The description of the process.
                id_short (Optional[str]): The short id of the process.
                semantic_id (Optional[str]): The semantic id of the process.
                general_type (Literal["Manufacturing", "Material Flow", "Remanufacturing", "Assembly",
            "Other"]): The general type of process or procedure that is describeded by this attribute.
                manufacturing_process_type (Optional[Literal["Primary Shaping", "Forming", "Cutting",
            "Joining", "Coating", "Changing Material Properties"]]): The type of manufacturing process
            according to DIN 8580.
                material_flow_process_type (Optional[Literal["Storage", "Handling", "Conveying"]]):
            The type of material flow process according to VDI 2411.
                remanufacturing_process_type (Optional[Literal["Disassembly", "Remediation",
            "Cleaning", "Inspection"]]): The type of remanufacturing process according to VDI 2243.
                assembly_process_type (Optional[Literal["Joining", "Handling", "Adjusting", "Testing",
            "Special Operations"]]): The type of assembly process according to VDI 2860.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError, PutItemProcessItemIdProcessInformationPutResponsePutItemProcessItemIdProcessinformationPut]]
    """

    kwargs = _get_kwargs(
        item_id=item_id,
        client=client,
        json_body=json_body,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    item_id: str,
    *,
    client: Client,
    json_body: ProcessInformation,
) -> Optional[
    Union[
        Any,
        HTTPValidationError,
        PutItemProcessItemIdProcessInformationPutResponsePutItemProcessItemIdProcessinformationPut,
    ]
]:
    """Put Item

    Args:
        item_id (str):
        json_body (ProcessInformation): The SubmodelElementCollection GeneralInfo contains 4
            SubmodelElements that allow to describe one specific process attribute in a structured,
            self-describing and interoperable way.
            The types are defined by DIN 8580 for Manufacturing Processes, VDI 2411 for Material Flow
            Processes, VDI 2243 for Remanufacturing Processes and VDI 2860 for Assembly.

            Args:
                id_ (str): The id of the general info.
                description (Optional[str]): The description of the process.
                id_short (Optional[str]): The short id of the process.
                semantic_id (Optional[str]): The semantic id of the process.
                general_type (Literal["Manufacturing", "Material Flow", "Remanufacturing", "Assembly",
            "Other"]): The general type of process or procedure that is describeded by this attribute.
                manufacturing_process_type (Optional[Literal["Primary Shaping", "Forming", "Cutting",
            "Joining", "Coating", "Changing Material Properties"]]): The type of manufacturing process
            according to DIN 8580.
                material_flow_process_type (Optional[Literal["Storage", "Handling", "Conveying"]]):
            The type of material flow process according to VDI 2411.
                remanufacturing_process_type (Optional[Literal["Disassembly", "Remediation",
            "Cleaning", "Inspection"]]): The type of remanufacturing process according to VDI 2243.
                assembly_process_type (Optional[Literal["Joining", "Handling", "Adjusting", "Testing",
            "Special Operations"]]): The type of assembly process according to VDI 2860.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError, PutItemProcessItemIdProcessInformationPutResponsePutItemProcessItemIdProcessinformationPut]
    """

    return sync_detailed(
        item_id=item_id,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    item_id: str,
    *,
    client: Client,
    json_body: ProcessInformation,
) -> Response[
    Union[
        Any,
        HTTPValidationError,
        PutItemProcessItemIdProcessInformationPutResponsePutItemProcessItemIdProcessinformationPut,
    ]
]:
    """Put Item

    Args:
        item_id (str):
        json_body (ProcessInformation): The SubmodelElementCollection GeneralInfo contains 4
            SubmodelElements that allow to describe one specific process attribute in a structured,
            self-describing and interoperable way.
            The types are defined by DIN 8580 for Manufacturing Processes, VDI 2411 for Material Flow
            Processes, VDI 2243 for Remanufacturing Processes and VDI 2860 for Assembly.

            Args:
                id_ (str): The id of the general info.
                description (Optional[str]): The description of the process.
                id_short (Optional[str]): The short id of the process.
                semantic_id (Optional[str]): The semantic id of the process.
                general_type (Literal["Manufacturing", "Material Flow", "Remanufacturing", "Assembly",
            "Other"]): The general type of process or procedure that is describeded by this attribute.
                manufacturing_process_type (Optional[Literal["Primary Shaping", "Forming", "Cutting",
            "Joining", "Coating", "Changing Material Properties"]]): The type of manufacturing process
            according to DIN 8580.
                material_flow_process_type (Optional[Literal["Storage", "Handling", "Conveying"]]):
            The type of material flow process according to VDI 2411.
                remanufacturing_process_type (Optional[Literal["Disassembly", "Remediation",
            "Cleaning", "Inspection"]]): The type of remanufacturing process according to VDI 2243.
                assembly_process_type (Optional[Literal["Joining", "Handling", "Adjusting", "Testing",
            "Special Operations"]]): The type of assembly process according to VDI 2860.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError, PutItemProcessItemIdProcessInformationPutResponsePutItemProcessItemIdProcessinformationPut]]
    """

    kwargs = _get_kwargs(
        item_id=item_id,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    item_id: str,
    *,
    client: Client,
    json_body: ProcessInformation,
) -> Optional[
    Union[
        Any,
        HTTPValidationError,
        PutItemProcessItemIdProcessInformationPutResponsePutItemProcessItemIdProcessinformationPut,
    ]
]:
    """Put Item

    Args:
        item_id (str):
        json_body (ProcessInformation): The SubmodelElementCollection GeneralInfo contains 4
            SubmodelElements that allow to describe one specific process attribute in a structured,
            self-describing and interoperable way.
            The types are defined by DIN 8580 for Manufacturing Processes, VDI 2411 for Material Flow
            Processes, VDI 2243 for Remanufacturing Processes and VDI 2860 for Assembly.

            Args:
                id_ (str): The id of the general info.
                description (Optional[str]): The description of the process.
                id_short (Optional[str]): The short id of the process.
                semantic_id (Optional[str]): The semantic id of the process.
                general_type (Literal["Manufacturing", "Material Flow", "Remanufacturing", "Assembly",
            "Other"]): The general type of process or procedure that is describeded by this attribute.
                manufacturing_process_type (Optional[Literal["Primary Shaping", "Forming", "Cutting",
            "Joining", "Coating", "Changing Material Properties"]]): The type of manufacturing process
            according to DIN 8580.
                material_flow_process_type (Optional[Literal["Storage", "Handling", "Conveying"]]):
            The type of material flow process according to VDI 2411.
                remanufacturing_process_type (Optional[Literal["Disassembly", "Remediation",
            "Cleaning", "Inspection"]]): The type of remanufacturing process according to VDI 2243.
                assembly_process_type (Optional[Literal["Joining", "Handling", "Adjusting", "Testing",
            "Special Operations"]]): The type of assembly process according to VDI 2860.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError, PutItemProcessItemIdProcessInformationPutResponsePutItemProcessItemIdProcessinformationPut]
    """

    return (
        await asyncio_detailed(
            item_id=item_id,
            client=client,
            json_body=json_body,
        )
    ).parsed
