from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import Client
from ...models.http_validation_error import HTTPValidationError
from ...models.order import Order
from ...models.put_item_order_item_id_put_response_put_item_order_item_id_put import (
    PutItemOrderItemIdPutResponsePutItemOrderItemIdPut,
)
from ...types import Response


def _get_kwargs(
    item_id: str,
    *,
    client: Client,
    json_body: Order,
) -> Dict[str, Any]:
    url = "{}/Order/{item_id}".format(client.base_url, item_id=item_id)

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
) -> Optional[Union[Any, HTTPValidationError, PutItemOrderItemIdPutResponsePutItemOrderItemIdPut]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = PutItemOrderItemIdPutResponsePutItemOrderItemIdPut.from_dict(response.json())

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
) -> Response[Union[Any, HTTPValidationError, PutItemOrderItemIdPutResponsePutItemOrderItemIdPut]]:
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
    json_body: Order,
) -> Response[Union[Any, HTTPValidationError, PutItemOrderItemIdPutResponsePutItemOrderItemIdPut]]:
    """Put Item

    Args:
        item_id (str):
        json_body (Order): AAS to describe an order.

            Args:
                id_ (str): The id of the order.
                description (Optional[str]): The description of the order.
                id_short (Optional[str]): The short id of the order.
                product_instances (ProductInstances): The product instances of the order.
                general_information (GeneralInformation): The general information of the order.
                order_schedule (OrderSchedule): The schedule of the order.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError, PutItemOrderItemIdPutResponsePutItemOrderItemIdPut]]
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
    json_body: Order,
) -> Optional[Union[Any, HTTPValidationError, PutItemOrderItemIdPutResponsePutItemOrderItemIdPut]]:
    """Put Item

    Args:
        item_id (str):
        json_body (Order): AAS to describe an order.

            Args:
                id_ (str): The id of the order.
                description (Optional[str]): The description of the order.
                id_short (Optional[str]): The short id of the order.
                product_instances (ProductInstances): The product instances of the order.
                general_information (GeneralInformation): The general information of the order.
                order_schedule (OrderSchedule): The schedule of the order.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError, PutItemOrderItemIdPutResponsePutItemOrderItemIdPut]
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
    json_body: Order,
) -> Response[Union[Any, HTTPValidationError, PutItemOrderItemIdPutResponsePutItemOrderItemIdPut]]:
    """Put Item

    Args:
        item_id (str):
        json_body (Order): AAS to describe an order.

            Args:
                id_ (str): The id of the order.
                description (Optional[str]): The description of the order.
                id_short (Optional[str]): The short id of the order.
                product_instances (ProductInstances): The product instances of the order.
                general_information (GeneralInformation): The general information of the order.
                order_schedule (OrderSchedule): The schedule of the order.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError, PutItemOrderItemIdPutResponsePutItemOrderItemIdPut]]
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
    json_body: Order,
) -> Optional[Union[Any, HTTPValidationError, PutItemOrderItemIdPutResponsePutItemOrderItemIdPut]]:
    """Put Item

    Args:
        item_id (str):
        json_body (Order): AAS to describe an order.

            Args:
                id_ (str): The id of the order.
                description (Optional[str]): The description of the order.
                id_short (Optional[str]): The short id of the order.
                product_instances (ProductInstances): The product instances of the order.
                general_information (GeneralInformation): The general information of the order.
                order_schedule (OrderSchedule): The schedule of the order.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError, PutItemOrderItemIdPutResponsePutItemOrderItemIdPut]
    """

    return (
        await asyncio_detailed(
            item_id=item_id,
            client=client,
            json_body=json_body,
        )
    ).parsed
