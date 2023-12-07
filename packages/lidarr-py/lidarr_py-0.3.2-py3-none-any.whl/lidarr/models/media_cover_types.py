# coding: utf-8

"""
    Lidarr

    Lidarr API docs  # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Generated by: https://openapi-generator.tech
"""


from inspect import getfullargspec
import pprint
import re  # noqa: F401
from aenum import Enum, no_arg





class MediaCoverTypes(str, Enum):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    allowed enum values
    """

    UNKNOWN = 'unknown'
    POSTER = 'poster'
    BANNER = 'banner'
    FANART = 'fanart'
    SCREENSHOT = 'screenshot'
    HEADSHOT = 'headshot'
    COVER = 'cover'
    DISC = 'disc'
    LOGO = 'logo'
    CLEARLOGO = 'clearlogo'

