#!/usr/bin/env python
# encoding: utf-8

"""This module contains functions for handling requests in relation to tags.
"""

from flask import current_app

from ec2stack import helpers, errors
from ec2stack.providers.cloudstack import requester


@helpers.authentication_required
def create_tags():
    """
    Create a tag.

    @return: Response.
    """
    _create_tag_request()
    return _create_tag_response()


def _create_tag_request():
    """
    Request to create a tag.

    @return: Response.
    """

    key = helpers.get('Tag.1.Key')
    value = helpers.get('Tag.1.Value')
    resource_id = helpers.get('ResourceId.1')

    if resource_id in current_app.config['RESOURCE_TYPE_MAP']:
        resource_type = current_app.config['RESOURCE_TYPE_MAP'][resource_id]
    else:
        errors.invalid_request(
            str(resource_id) +
            " not found in configuration")

    args = {
        'command': 'createTags',
        'resourceIds': resource_id,
        'resourceType': resource_type,
        'tags[0].key': key,
        'tags[0].value': value
    }

    response = requester.make_request_async(args)

    response = response['createtagsresponse']

    return response


def _create_tag_response():
    """
    Generates a response for a create tag request.

    @return: Response.
    """
    return {
        'template_name_or_list': 'status.xml',
        'response_type': 'CreateTagsResponse',
        'return': 'true'
    }


@helpers.authentication_required
def delete_tags():
    """
    delete a tag.

    @return: Response.
    """
    _delete_tag_request()
    return _delete_tag_response()


def _delete_tag_request():
    """
    Request to delete a tag.

    @return: Response.
    """
    key = helpers.get('Tag.1.Key')
    resource_id = helpers.get('ResourceId.1')

    args = {
        'command': 'deleteTag',
        'resourceIds': resource_id,
        'tags[0].key': key
    }

    response = requester.make_request_async(args)

    response = response['deletetagsresponse']

    return response


def _delete_tag_response():
    """
    Generates a response for a delete tag request.

    @return: Response.
    """
    return {
        'template_name_or_list': 'status.xml',
        'response_type': 'DeleteTagsResponse',
        'return': 'true'
    }


@helpers.authentication_required
def describe_tags():
    """
    Describe all tags.

    @return: Response.
    """
    args = {'command': 'listTags'}
    response = requester.make_request(args)

    return _describe_tags_response(
        response
    )


def _describe_tags_response(response):
    """
    Generates a response for a describe tags request.

    @param response: Response from Cloudstack.
    @return: Response.
    """
    return {
        'template_name_or_list': 'tags.xml',
        'response_type': 'DescribeTagsResponse',
        'response': response
    }
