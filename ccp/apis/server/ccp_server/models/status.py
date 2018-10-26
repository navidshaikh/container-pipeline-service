# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from ccp.apis.server.ccp_server.models.base_model_ import Model
from ccp.apis.server.ccp_server.models.meta import Meta  # noqa: F401,E501
from ccp.apis.server.ccp_server import util


class Status(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, meta: Meta = None, status: str = None):  # noqa: E501
        """Status - a model defined in Swagger

        :param meta: The meta of this Status.  # noqa: E501
        :type meta: Meta
        :param status: The status of this Status.  # noqa: E501
        :type status: str
        """
        self.swagger_types = {
            'meta': Meta,
            'status': str
        }

        self.attribute_map = {
            'meta': 'meta',
            'status': 'status'
        }

        self._meta = meta
        self._status = status

    @classmethod
    def from_dict(cls, dikt) -> 'Status':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Status of this Status.  # noqa: E501
        :rtype: Status
        """
        return util.deserialize_model(dikt, cls)

    @property
    def meta(self) -> Meta:
        """Gets the meta of this Status.


        :return: The meta of this Status.
        :rtype: Meta
        """
        return self._meta

    @meta.setter
    def meta(self, meta: Meta):
        """Sets the meta of this Status.


        :param meta: The meta of this Status.
        :type meta: Meta
        """

        self._meta = meta

    @property
    def status(self) -> str:
        """Gets the status of this Status.


        :return: The status of this Status.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status: str):
        """Sets the status of this Status.


        :param status: The status of this Status.
        :type status: str
        """

        self._status = status
