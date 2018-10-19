# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from ccp.apis.server.ccp_server.models.base_model_ import Model
from ccp.apis.server.ccp_server.models.meta import Meta  # noqa: F401,E501
from ccp.apis.server.ccp_server.models.project_weekly_scan_builds import\
    ProjectWeeklyScanBuilds  # noqa: F401,E501
from ccp.apis.server.ccp_server import util


class WeeklyScanBuildsInfo(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, meta: Meta=None, wscan_builds: ProjectWeeklyScanBuilds=None):  # noqa: E501
        """WeeklyScanBuildsInfo - a model defined in Swagger

        :param meta: The meta of this WeeklyScanBuildsInfo.  # noqa: E501
        :type meta: Meta
        :param wscan_builds: The wscan_builds of this WeeklyScanBuildsInfo.  # noqa: E501
        :type wscan_builds: ProjectWeeklyScanBuilds
        """
        self.swagger_types = {
            'meta': Meta,
            'wscan_builds': ProjectWeeklyScanBuilds
        }

        self.attribute_map = {
            'meta': 'meta',
            'wscan_builds': 'wscan-builds'
        }

        self._meta = meta
        self._wscan_builds = wscan_builds

    @classmethod
    def from_dict(cls, dikt) -> 'WeeklyScanBuildsInfo':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The WeeklyScanBuildsInfo of this WeeklyScanBuildsInfo.  # noqa: E501
        :rtype: WeeklyScanBuildsInfo
        """
        return util.deserialize_model(dikt, cls)

    @property
    def meta(self) -> Meta:
        """Gets the meta of this WeeklyScanBuildsInfo.


        :return: The meta of this WeeklyScanBuildsInfo.
        :rtype: Meta
        """
        return self._meta

    @meta.setter
    def meta(self, meta: Meta):
        """Sets the meta of this WeeklyScanBuildsInfo.


        :param meta: The meta of this WeeklyScanBuildsInfo.
        :type meta: Meta
        """

        self._meta = meta

    @property
    def wscan_builds(self) -> ProjectWeeklyScanBuilds:
        """Gets the wscan_builds of this WeeklyScanBuildsInfo.


        :return: The wscan_builds of this WeeklyScanBuildsInfo.
        :rtype: ProjectWeeklyScanBuilds
        """
        return self._wscan_builds

    @wscan_builds.setter
    def wscan_builds(self, wscan_builds: ProjectWeeklyScanBuilds):
        """Sets the wscan_builds of this WeeklyScanBuildsInfo.


        :param wscan_builds: The wscan_builds of this WeeklyScanBuildsInfo.
        :type wscan_builds: ProjectWeeklyScanBuilds
        """

        self._wscan_builds = wscan_builds
