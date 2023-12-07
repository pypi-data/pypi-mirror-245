from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import Client
from ...models.http_validation_error import HTTPValidationError
from ...models.post_item_product_post_response_post_item_product_post import (
    PostItemProductPostResponsePostItemProductPost,
)
from ...models.product import Product
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    json_body: Product,
) -> Dict[str, Any]:
    url = "{}/Product/".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "json": json_json_body,
    }


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Optional[Union[Any, HTTPValidationError, PostItemProductPostResponsePostItemProductPost]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = PostItemProductPostResponsePostItemProductPost.from_dict(response.json())

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
) -> Response[Union[Any, HTTPValidationError, PostItemProductPostResponsePostItemProductPost]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    json_body: Product,
) -> Response[Union[Any, HTTPValidationError, PostItemProductPostResponsePostItemProductPost]]:
    """Post Item

    Args:
        json_body (Product): AAS to describe a product.

            Args:
                id_ (str): The id of the product.
                description (Optional[str]): The description of the product.
                id_short (Optional[str]): The short id of the product.
                semantic_id (Optional[str]): The semantic id of the product.
                construction_data (Optional[ConstructionData]): The construction data of the product.
                bom (Optional[BOM]): The bill of materials of the product.
                process_reference (Optional[ProcessReference]): The process reference of the product.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError, PostItemProductPostResponsePostItemProductPost]]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Client,
    json_body: Product,
) -> Optional[Union[Any, HTTPValidationError, PostItemProductPostResponsePostItemProductPost]]:
    """Post Item

    Args:
        json_body (Product): AAS to describe a product.

            Args:
                id_ (str): The id of the product.
                description (Optional[str]): The description of the product.
                id_short (Optional[str]): The short id of the product.
                semantic_id (Optional[str]): The semantic id of the product.
                construction_data (Optional[ConstructionData]): The construction data of the product.
                bom (Optional[BOM]): The bill of materials of the product.
                process_reference (Optional[ProcessReference]): The process reference of the product.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError, PostItemProductPostResponsePostItemProductPost]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    json_body: Product,
) -> Response[Union[Any, HTTPValidationError, PostItemProductPostResponsePostItemProductPost]]:
    """Post Item

    Args:
        json_body (Product): AAS to describe a product.

            Args:
                id_ (str): The id of the product.
                description (Optional[str]): The description of the product.
                id_short (Optional[str]): The short id of the product.
                semantic_id (Optional[str]): The semantic id of the product.
                construction_data (Optional[ConstructionData]): The construction data of the product.
                bom (Optional[BOM]): The bill of materials of the product.
                process_reference (Optional[ProcessReference]): The process reference of the product.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError, PostItemProductPostResponsePostItemProductPost]]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
    json_body: Product,
) -> Optional[Union[Any, HTTPValidationError, PostItemProductPostResponsePostItemProductPost]]:
    """Post Item

    Args:
        json_body (Product): AAS to describe a product.

            Args:
                id_ (str): The id of the product.
                description (Optional[str]): The description of the product.
                id_short (Optional[str]): The short id of the product.
                semantic_id (Optional[str]): The semantic id of the product.
                construction_data (Optional[ConstructionData]): The construction data of the product.
                bom (Optional[BOM]): The bill of materials of the product.
                process_reference (Optional[ProcessReference]): The process reference of the product.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError, PostItemProductPostResponsePostItemProductPost]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
