"""Create a new data element in a data dictionary"""
from http import HTTPStatus
from typing import Any
from typing import Dict
from typing import Union

import httpx

from ... import errors
from ...client import AuthenticatedClient
from ...client import Client
from ...models.collections_dictionaries_create_a_new_data_element_data_element import (
    CollectionsDictionariesCreateANewDataElementDataElement,
)
from ...models.data_element import DataElement
from ...models.server_error import ServerError
from ...types import Response


def _get_kwargs(
    collection_id: str,
    version_id: str,
    item_id: str,
    *,
    json_body: CollectionsDictionariesCreateANewDataElementDataElement,
) -> Dict[str, Any]:
    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/collections/{collection_id}/{version_id}/dictionaries/{item_id}/elements".format(
            collection_id=collection_id,
            version_id=version_id,
            item_id=item_id,
        ),
        "json": json_json_body,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[DataElement, ServerError]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = DataElement.from_dict(response.json())

        return response_201
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = ServerError.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = ServerError.from_dict(response.json())

        return response_401
    if response.status_code == HTTPStatus.FORBIDDEN:
        response_403 = ServerError.from_dict(response.json())

        return response_403
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = ServerError.from_dict(response.json())

        return response_404
    if response.status_code == HTTPStatus.UNSUPPORTED_MEDIA_TYPE:
        response_415 = ServerError.from_dict(response.json())

        return response_415
    if response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        response_500 = ServerError.from_dict(response.json())

        return response_500

    raise errors.UnexpectedStatus(response.status_code, response.content)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[DataElement, ServerError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    collection_id: str,
    version_id: str,
    item_id: str,
    *,
    client: AuthenticatedClient,
    json_body: CollectionsDictionariesCreateANewDataElementDataElement,
) -> Response[Union[DataElement, ServerError]]:
    """Create a new data element in a data dictionary

    TODO

    Args:
        collection_id (str):
        version_id (str):
        item_id (str):
        json_body (CollectionsDictionariesCreateANewDataElementDataElement): Pigeon Data Element

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DataElement, ServerError]]
    """

    kwargs = _get_kwargs(
        collection_id=collection_id,
        version_id=version_id,
        item_id=item_id,
        json_body=json_body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    collection_id: str,
    version_id: str,
    item_id: str,
    *,
    client: AuthenticatedClient,
    json_body: CollectionsDictionariesCreateANewDataElementDataElement,
) -> Union[DataElement]:
    """Create a new data element in a data dictionary

    TODO

    Args:
        collection_id (str):
        version_id (str):
        item_id (str):
        json_body (CollectionsDictionariesCreateANewDataElementDataElement): Pigeon Data Element

    Raises:
        errors.UnexpectedStatus: If the server returns a status code greater than or equal to 300.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DataElement]
    """

    response = sync_detailed(
        collection_id=collection_id,
        version_id=version_id,
        item_id=item_id,
        client=client,
        json_body=json_body,
    )
    if isinstance(response.parsed, ServerError):
        raise errors.UnexpectedStatus(response.status_code, response.content)

    return response.parsed


async def asyncio_detailed(
    collection_id: str,
    version_id: str,
    item_id: str,
    *,
    client: AuthenticatedClient,
    json_body: CollectionsDictionariesCreateANewDataElementDataElement,
) -> Response[Union[DataElement, ServerError]]:
    """Create a new data element in a data dictionary

    TODO

    Args:
        collection_id (str):
        version_id (str):
        item_id (str):
        json_body (CollectionsDictionariesCreateANewDataElementDataElement): Pigeon Data Element

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DataElement, ServerError]]
    """

    kwargs = _get_kwargs(
        collection_id=collection_id,
        version_id=version_id,
        item_id=item_id,
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    collection_id: str,
    version_id: str,
    item_id: str,
    *,
    client: AuthenticatedClient,
    json_body: CollectionsDictionariesCreateANewDataElementDataElement,
) -> Union[DataElement]:
    """Create a new data element in a data dictionary

    TODO

    Args:
        collection_id (str):
        version_id (str):
        item_id (str):
        json_body (CollectionsDictionariesCreateANewDataElementDataElement): Pigeon Data Element

    Raises:
        errors.UnexpectedStatus: If the server returns a status code greater than or equal to 300.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DataElement]
    """

    response = await asyncio_detailed(
        collection_id=collection_id,
        version_id=version_id,
        item_id=item_id,
        client=client,
        json_body=json_body,
    )
    if isinstance(response.parsed, ServerError):
        raise errors.UnexpectedStatus(response.status_code, response.content)

    return response.parsed
