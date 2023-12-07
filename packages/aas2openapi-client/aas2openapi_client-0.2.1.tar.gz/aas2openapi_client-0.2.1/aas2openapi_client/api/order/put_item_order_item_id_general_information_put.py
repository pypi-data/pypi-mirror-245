from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import Client
from ...models.general_information import GeneralInformation
from ...models.http_validation_error import HTTPValidationError
from ...models.put_item_order_item_id_general_information_put_response_put_item_order_item_id_generalinformation_put import (
    PutItemOrderItemIdGeneralInformationPutResponsePutItemOrderItemIdGeneralinformationPut,
)
from ...types import Response


def _get_kwargs(
    item_id: str,
    *,
    client: Client,
    json_body: GeneralInformation,
) -> Dict[str, Any]:
    url = "{}/Order/{item_id}/GeneralInformation/".format(client.base_url, item_id=item_id)

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
        Any, HTTPValidationError, PutItemOrderItemIdGeneralInformationPutResponsePutItemOrderItemIdGeneralinformationPut
    ]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = PutItemOrderItemIdGeneralInformationPutResponsePutItemOrderItemIdGeneralinformationPut.from_dict(
            response.json()
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
        Any, HTTPValidationError, PutItemOrderItemIdGeneralInformationPutResponsePutItemOrderItemIdGeneralinformationPut
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
    json_body: GeneralInformation,
) -> Response[
    Union[
        Any, HTTPValidationError, PutItemOrderItemIdGeneralInformationPutResponsePutItemOrderItemIdGeneralinformationPut
    ]
]:
    """Put Item

    Args:
        item_id (str):
        json_body (GeneralInformation): Submodel to describe the general information of an order.

            Args:
                id_ (str): The id of the general information.
                description (Optional[str]): The description of the general information.
                id_short (Optional[str]): The short id of the general information.
                semantic_id (Optional[str]): The semantic id of the general information.
                order_id (str): The id of the order.
                priority (int): The priority of the order.
                customer_information (str): The customer information of the order.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError, PutItemOrderItemIdGeneralInformationPutResponsePutItemOrderItemIdGeneralinformationPut]]
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
    json_body: GeneralInformation,
) -> Optional[
    Union[
        Any, HTTPValidationError, PutItemOrderItemIdGeneralInformationPutResponsePutItemOrderItemIdGeneralinformationPut
    ]
]:
    """Put Item

    Args:
        item_id (str):
        json_body (GeneralInformation): Submodel to describe the general information of an order.

            Args:
                id_ (str): The id of the general information.
                description (Optional[str]): The description of the general information.
                id_short (Optional[str]): The short id of the general information.
                semantic_id (Optional[str]): The semantic id of the general information.
                order_id (str): The id of the order.
                priority (int): The priority of the order.
                customer_information (str): The customer information of the order.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError, PutItemOrderItemIdGeneralInformationPutResponsePutItemOrderItemIdGeneralinformationPut]
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
    json_body: GeneralInformation,
) -> Response[
    Union[
        Any, HTTPValidationError, PutItemOrderItemIdGeneralInformationPutResponsePutItemOrderItemIdGeneralinformationPut
    ]
]:
    """Put Item

    Args:
        item_id (str):
        json_body (GeneralInformation): Submodel to describe the general information of an order.

            Args:
                id_ (str): The id of the general information.
                description (Optional[str]): The description of the general information.
                id_short (Optional[str]): The short id of the general information.
                semantic_id (Optional[str]): The semantic id of the general information.
                order_id (str): The id of the order.
                priority (int): The priority of the order.
                customer_information (str): The customer information of the order.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError, PutItemOrderItemIdGeneralInformationPutResponsePutItemOrderItemIdGeneralinformationPut]]
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
    json_body: GeneralInformation,
) -> Optional[
    Union[
        Any, HTTPValidationError, PutItemOrderItemIdGeneralInformationPutResponsePutItemOrderItemIdGeneralinformationPut
    ]
]:
    """Put Item

    Args:
        item_id (str):
        json_body (GeneralInformation): Submodel to describe the general information of an order.

            Args:
                id_ (str): The id of the general information.
                description (Optional[str]): The description of the general information.
                id_short (Optional[str]): The short id of the general information.
                semantic_id (Optional[str]): The semantic id of the general information.
                order_id (str): The id of the order.
                priority (int): The priority of the order.
                customer_information (str): The customer information of the order.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError, PutItemOrderItemIdGeneralInformationPutResponsePutItemOrderItemIdGeneralinformationPut]
    """

    return (
        await asyncio_detailed(
            item_id=item_id,
            client=client,
            json_body=json_body,
        )
    ).parsed
