# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from ccp.apis.server.ccp_server.models.base_model_ import Model
from ccp.apis.server.ccp_server import util


class ProjectWeeklyScanBuildNameStatus(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, weeklyscan_build: str=None, status: str=None):  # noqa: E501
        """ProjectWeeklyScanBuildNameStatus - a model defined in Swagger

        :param weeklyscan_build: The weeklyscan_build of this ProjectWeeklyScanBuildNameStatus.  # noqa: E501
        :type weeklyscan_build: str
        :param status: The status of this ProjectWeeklyScanBuildNameStatus.  # noqa: E501
        :type status: str
        """
        self.swagger_types = {
            'weeklyscan_build': str,
            'status': str
        }

        self.attribute_map = {
            'weeklyscan_build': 'weeklyscan-build',
            'status': 'status'
        }

        self._weeklyscan_build = weeklyscan_build
        self._status = status

    @classmethod
    def from_dict(cls, dikt) -> 'ProjectWeeklyScanBuildNameStatus':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The ProjectWeeklyScanBuildNameStatus of this ProjectWeeklyScanBuildNameStatus.  # noqa: E501
        :rtype: ProjectWeeklyScanBuildNameStatus
        """
        return util.deserialize_model(dikt, cls)

    @property
    def weeklyscan_build(self) -> str:
        """Gets the weeklyscan_build of this ProjectWeeklyScanBuildNameStatus.


        :return: The weeklyscan_build of this ProjectWeeklyScanBuildNameStatus.
        :rtype: str
        """
        return self._weeklyscan_build

    @weeklyscan_build.setter
    def weeklyscan_build(self, weeklyscan_build: str):
        """Sets the weeklyscan_build of this ProjectWeeklyScanBuildNameStatus.


        :param weeklyscan_build: The weeklyscan_build of this ProjectWeeklyScanBuildNameStatus.
        :type weeklyscan_build: str
        """

        self._weeklyscan_build = weeklyscan_build

    @property
    def status(self) -> str:
        """Gets the status of this ProjectWeeklyScanBuildNameStatus.


        :return: The status of this ProjectWeeklyScanBuildNameStatus.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status: str):
        """Sets the status of this ProjectWeeklyScanBuildNameStatus.


        :param status: The status of this ProjectWeeklyScanBuildNameStatus.
        :type status: str
        """

        self._status = status
