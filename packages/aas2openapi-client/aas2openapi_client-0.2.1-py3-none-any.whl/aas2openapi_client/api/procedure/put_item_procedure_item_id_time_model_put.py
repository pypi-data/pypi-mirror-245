from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import Client
from ...models.http_validation_error import HTTPValidationError
from ...models.put_item_procedure_item_id_time_model_put_response_put_item_procedure_item_id_timemodel_put import (
    PutItemProcedureItemIdTimeModelPutResponsePutItemProcedureItemIdTimemodelPut,
)
from ...models.time_model import TimeModel
from ...types import Response


def _get_kwargs(
    item_id: str,
    *,
    client: Client,
    json_body: TimeModel,
) -> Dict[str, Any]:
    url = "{}/Procedure/{item_id}/TimeModel/".format(client.base_url, item_id=item_id)

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
    Union[Any, HTTPValidationError, PutItemProcedureItemIdTimeModelPutResponsePutItemProcedureItemIdTimemodelPut]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = PutItemProcedureItemIdTimeModelPutResponsePutItemProcedureItemIdTimemodelPut.from_dict(
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
    Union[Any, HTTPValidationError, PutItemProcedureItemIdTimeModelPutResponsePutItemProcedureItemIdTimemodelPut]
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
    json_body: TimeModel,
) -> Response[
    Union[Any, HTTPValidationError, PutItemProcedureItemIdTimeModelPutResponsePutItemProcedureItemIdTimemodelPut]
]:
    """Put Item

    Args:
        item_id (str):
        json_body (TimeModel): Submodel containing parameters to represent the timely duration of
            a procedure.

            Args:
                id_ (str): The id of the time model.
                description (Optional[str]): The description of the time model.
                id_short (Optional[str]): The short id of the time model.
                semantic_id (Optional[str]): The semantic id of the time model.
                type_ (Literal["sequential", "distribution", "distance_based"]): The type of the time
            model.
                sequence (Optional[List[float]]): The sequence of timely values (only for sequential
            time models).
                repeat (Optional[bool]): Whether the sequence is repeated or not (only for sequential
            time models).
                distribution_type (Optional[str]): The name of the distribution (e.g. "normal",
            "exponential", "weibull", "lognormal", "gamma", "beta", "uniform", "triangular",
            "discrete") (only for distribution time models).
                distribution_parameters (Optional[List[float]]): The parameters of the distribution
            (1: location, 2: scale, 3 and 4: shape) (only for distribution time models).
                speed (Optional[float]): The speed of the resource (only for distance-based time
            models).
                reaction_time (Optional[float]): The reaction time of the resource (only for distance-
            based time models).
                acceleration (Optional[float]): The acceleration of the resource (only for distance-
            based time models).
                deceleration (Optional[float]): The deceleration of the resource (only for distance-
            based time models).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError, PutItemProcedureItemIdTimeModelPutResponsePutItemProcedureItemIdTimemodelPut]]
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
    json_body: TimeModel,
) -> Optional[
    Union[Any, HTTPValidationError, PutItemProcedureItemIdTimeModelPutResponsePutItemProcedureItemIdTimemodelPut]
]:
    """Put Item

    Args:
        item_id (str):
        json_body (TimeModel): Submodel containing parameters to represent the timely duration of
            a procedure.

            Args:
                id_ (str): The id of the time model.
                description (Optional[str]): The description of the time model.
                id_short (Optional[str]): The short id of the time model.
                semantic_id (Optional[str]): The semantic id of the time model.
                type_ (Literal["sequential", "distribution", "distance_based"]): The type of the time
            model.
                sequence (Optional[List[float]]): The sequence of timely values (only for sequential
            time models).
                repeat (Optional[bool]): Whether the sequence is repeated or not (only for sequential
            time models).
                distribution_type (Optional[str]): The name of the distribution (e.g. "normal",
            "exponential", "weibull", "lognormal", "gamma", "beta", "uniform", "triangular",
            "discrete") (only for distribution time models).
                distribution_parameters (Optional[List[float]]): The parameters of the distribution
            (1: location, 2: scale, 3 and 4: shape) (only for distribution time models).
                speed (Optional[float]): The speed of the resource (only for distance-based time
            models).
                reaction_time (Optional[float]): The reaction time of the resource (only for distance-
            based time models).
                acceleration (Optional[float]): The acceleration of the resource (only for distance-
            based time models).
                deceleration (Optional[float]): The deceleration of the resource (only for distance-
            based time models).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError, PutItemProcedureItemIdTimeModelPutResponsePutItemProcedureItemIdTimemodelPut]
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
    json_body: TimeModel,
) -> Response[
    Union[Any, HTTPValidationError, PutItemProcedureItemIdTimeModelPutResponsePutItemProcedureItemIdTimemodelPut]
]:
    """Put Item

    Args:
        item_id (str):
        json_body (TimeModel): Submodel containing parameters to represent the timely duration of
            a procedure.

            Args:
                id_ (str): The id of the time model.
                description (Optional[str]): The description of the time model.
                id_short (Optional[str]): The short id of the time model.
                semantic_id (Optional[str]): The semantic id of the time model.
                type_ (Literal["sequential", "distribution", "distance_based"]): The type of the time
            model.
                sequence (Optional[List[float]]): The sequence of timely values (only for sequential
            time models).
                repeat (Optional[bool]): Whether the sequence is repeated or not (only for sequential
            time models).
                distribution_type (Optional[str]): The name of the distribution (e.g. "normal",
            "exponential", "weibull", "lognormal", "gamma", "beta", "uniform", "triangular",
            "discrete") (only for distribution time models).
                distribution_parameters (Optional[List[float]]): The parameters of the distribution
            (1: location, 2: scale, 3 and 4: shape) (only for distribution time models).
                speed (Optional[float]): The speed of the resource (only for distance-based time
            models).
                reaction_time (Optional[float]): The reaction time of the resource (only for distance-
            based time models).
                acceleration (Optional[float]): The acceleration of the resource (only for distance-
            based time models).
                deceleration (Optional[float]): The deceleration of the resource (only for distance-
            based time models).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError, PutItemProcedureItemIdTimeModelPutResponsePutItemProcedureItemIdTimemodelPut]]
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
    json_body: TimeModel,
) -> Optional[
    Union[Any, HTTPValidationError, PutItemProcedureItemIdTimeModelPutResponsePutItemProcedureItemIdTimemodelPut]
]:
    """Put Item

    Args:
        item_id (str):
        json_body (TimeModel): Submodel containing parameters to represent the timely duration of
            a procedure.

            Args:
                id_ (str): The id of the time model.
                description (Optional[str]): The description of the time model.
                id_short (Optional[str]): The short id of the time model.
                semantic_id (Optional[str]): The semantic id of the time model.
                type_ (Literal["sequential", "distribution", "distance_based"]): The type of the time
            model.
                sequence (Optional[List[float]]): The sequence of timely values (only for sequential
            time models).
                repeat (Optional[bool]): Whether the sequence is repeated or not (only for sequential
            time models).
                distribution_type (Optional[str]): The name of the distribution (e.g. "normal",
            "exponential", "weibull", "lognormal", "gamma", "beta", "uniform", "triangular",
            "discrete") (only for distribution time models).
                distribution_parameters (Optional[List[float]]): The parameters of the distribution
            (1: location, 2: scale, 3 and 4: shape) (only for distribution time models).
                speed (Optional[float]): The speed of the resource (only for distance-based time
            models).
                reaction_time (Optional[float]): The reaction time of the resource (only for distance-
            based time models).
                acceleration (Optional[float]): The acceleration of the resource (only for distance-
            based time models).
                deceleration (Optional[float]): The deceleration of the resource (only for distance-
            based time models).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError, PutItemProcedureItemIdTimeModelPutResponsePutItemProcedureItemIdTimemodelPut]
    """

    return (
        await asyncio_detailed(
            item_id=item_id,
            client=client,
            json_body=json_body,
        )
    ).parsed
