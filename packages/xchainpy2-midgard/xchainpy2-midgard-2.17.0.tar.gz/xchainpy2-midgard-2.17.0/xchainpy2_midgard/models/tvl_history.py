# coding: utf-8

"""
    Midgard Public API

    The Midgard Public API queries THORChain and any chains linked via the Bifröst and prepares information about the network to be readily available for public users. The API parses transaction event data from THORChain and stores them in a time-series database to make time-dependent queries easy. Midgard does not hold critical information. To interact with THORChain protocol, users should query THORNode directly.  # noqa: E501

    OpenAPI spec version: 2.17.0
    Contact: devs@thorchain.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class TVLHistory(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'intervals': 'TVLHistoryIntervals',
        'meta': 'TVLHistoryItem'
    }

    attribute_map = {
        'intervals': 'intervals',
        'meta': 'meta'
    }

    def __init__(self, intervals=None, meta=None):  # noqa: E501
        """TVLHistory - a model defined in Swagger"""  # noqa: E501
        self._intervals = None
        self._meta = None
        self.discriminator = None
        self.intervals = intervals
        self.meta = meta

    @property
    def intervals(self):
        """Gets the intervals of this TVLHistory.  # noqa: E501


        :return: The intervals of this TVLHistory.  # noqa: E501
        :rtype: TVLHistoryIntervals
        """
        return self._intervals

    @intervals.setter
    def intervals(self, intervals):
        """Sets the intervals of this TVLHistory.


        :param intervals: The intervals of this TVLHistory.  # noqa: E501
        :type: TVLHistoryIntervals
        """
        if intervals is None:
            raise ValueError("Invalid value for `intervals`, must not be `None`")  # noqa: E501

        self._intervals = intervals

    @property
    def meta(self):
        """Gets the meta of this TVLHistory.  # noqa: E501


        :return: The meta of this TVLHistory.  # noqa: E501
        :rtype: TVLHistoryItem
        """
        return self._meta

    @meta.setter
    def meta(self, meta):
        """Sets the meta of this TVLHistory.


        :param meta: The meta of this TVLHistory.  # noqa: E501
        :type: TVLHistoryItem
        """
        if meta is None:
            raise ValueError("Invalid value for `meta`, must not be `None`")  # noqa: E501

        self._meta = meta

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(TVLHistory, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, TVLHistory):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
