from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import Client
from ...models.http_validation_error import HTTPValidationError
from ...models.process_attributes import ProcessAttributes
from ...models.put_item_process_item_id_process_attributes_put_response_put_item_process_item_id_processattributes_put import (
    PutItemProcessItemIdProcessAttributesPutResponsePutItemProcessItemIdProcessattributesPut,
)
from ...types import Response


def _get_kwargs(
    item_id: str,
    *,
    client: Client,
    json_body: ProcessAttributes,
) -> Dict[str, Any]:
    url = "{}/Process/{item_id}/ProcessAttributes/".format(client.base_url, item_id=item_id)

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
        PutItemProcessItemIdProcessAttributesPutResponsePutItemProcessItemIdProcessattributesPut,
    ]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = (
            PutItemProcessItemIdProcessAttributesPutResponsePutItemProcessItemIdProcessattributesPut.from_dict(
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
        PutItemProcessItemIdProcessAttributesPutResponsePutItemProcessItemIdProcessattributesPut,
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
    json_body: ProcessAttributes,
) -> Response[
    Union[
        Any,
        HTTPValidationError,
        PutItemProcessItemIdProcessAttributesPutResponsePutItemProcessItemIdProcessattributesPut,
    ]
]:
    """Put Item

    Args:
        item_id (str):
        json_body (ProcessAttributes): The SubmodelElementCollection “ProcessAttributes” contains
            4 SubmodelElements that allow to describe one specific process attribute in a structured,
            self-describing and interoperable way.

            Args:
                id_ (str): The id of the process attributes.
                description (Optional[str]): The description of the process attributes.
                id_short (Optional[str]): The short id of the process attributes.
                semantic_id (Optional[str]): The semantic id of the process attributes.
                process_attributes (List[AttributePredicate]): The process attributes of the process
            (e.g. rotation speed, ...)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError, PutItemProcessItemIdProcessAttributesPutResponsePutItemProcessItemIdProcessattributesPut]]
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
    json_body: ProcessAttributes,
) -> Optional[
    Union[
        Any,
        HTTPValidationError,
        PutItemProcessItemIdProcessAttributesPutResponsePutItemProcessItemIdProcessattributesPut,
    ]
]:
    """Put Item

    Args:
        item_id (str):
        json_body (ProcessAttributes): The SubmodelElementCollection “ProcessAttributes” contains
            4 SubmodelElements that allow to describe one specific process attribute in a structured,
            self-describing and interoperable way.

            Args:
                id_ (str): The id of the process attributes.
                description (Optional[str]): The description of the process attributes.
                id_short (Optional[str]): The short id of the process attributes.
                semantic_id (Optional[str]): The semantic id of the process attributes.
                process_attributes (List[AttributePredicate]): The process attributes of the process
            (e.g. rotation speed, ...)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError, PutItemProcessItemIdProcessAttributesPutResponsePutItemProcessItemIdProcessattributesPut]
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
    json_body: ProcessAttributes,
) -> Response[
    Union[
        Any,
        HTTPValidationError,
        PutItemProcessItemIdProcessAttributesPutResponsePutItemProcessItemIdProcessattributesPut,
    ]
]:
    """Put Item

    Args:
        item_id (str):
        json_body (ProcessAttributes): The SubmodelElementCollection “ProcessAttributes” contains
            4 SubmodelElements that allow to describe one specific process attribute in a structured,
            self-describing and interoperable way.

            Args:
                id_ (str): The id of the process attributes.
                description (Optional[str]): The description of the process attributes.
                id_short (Optional[str]): The short id of the process attributes.
                semantic_id (Optional[str]): The semantic id of the process attributes.
                process_attributes (List[AttributePredicate]): The process attributes of the process
            (e.g. rotation speed, ...)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError, PutItemProcessItemIdProcessAttributesPutResponsePutItemProcessItemIdProcessattributesPut]]
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
    json_body: ProcessAttributes,
) -> Optional[
    Union[
        Any,
        HTTPValidationError,
        PutItemProcessItemIdProcessAttributesPutResponsePutItemProcessItemIdProcessattributesPut,
    ]
]:
    """Put Item

    Args:
        item_id (str):
        json_body (ProcessAttributes): The SubmodelElementCollection “ProcessAttributes” contains
            4 SubmodelElements that allow to describe one specific process attribute in a structured,
            self-describing and interoperable way.

            Args:
                id_ (str): The id of the process attributes.
                description (Optional[str]): The description of the process attributes.
                id_short (Optional[str]): The short id of the process attributes.
                semantic_id (Optional[str]): The semantic id of the process attributes.
                process_attributes (List[AttributePredicate]): The process attributes of the process
            (e.g. rotation speed, ...)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError, PutItemProcessItemIdProcessAttributesPutResponsePutItemProcessItemIdProcessattributesPut]
    """

    return (
        await asyncio_detailed(
            item_id=item_id,
            client=client,
            json_body=json_body,
        )
    ).parsed
