# coding: utf-8

"""
    osparc.io web API (dev)

    osparc-simcore public API specifications  # noqa: E501

    The version of the OpenAPI document: 0.5.0-dev
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from osparc_client.configuration import Configuration


class OnePageStudyPort(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'items': 'list[StudyPort]',
        'total': 'int'
    }

    attribute_map = {
        'items': 'items',
        'total': 'total'
    }

    def __init__(self, items=None, total=None, local_vars_configuration=None):  # noqa: E501
        """OnePageStudyPort - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._items = None
        self._total = None
        self.discriminator = None

        self.items = items
        if total is not None:
            self.total = total

    @property
    def items(self):
        """Gets the items of this OnePageStudyPort.  # noqa: E501


        :return: The items of this OnePageStudyPort.  # noqa: E501
        :rtype: list[StudyPort]
        """
        return self._items

    @items.setter
    def items(self, items):
        """Sets the items of this OnePageStudyPort.


        :param items: The items of this OnePageStudyPort.  # noqa: E501
        :type: list[StudyPort]
        """
        if self.local_vars_configuration.client_side_validation and items is None:  # noqa: E501
            raise ValueError("Invalid value for `items`, must not be `None`")  # noqa: E501

        self._items = items

    @property
    def total(self):
        """Gets the total of this OnePageStudyPort.  # noqa: E501


        :return: The total of this OnePageStudyPort.  # noqa: E501
        :rtype: int
        """
        return self._total

    @total.setter
    def total(self, total):
        """Sets the total of this OnePageStudyPort.


        :param total: The total of this OnePageStudyPort.  # noqa: E501
        :type: int
        """
        if (self.local_vars_configuration.client_side_validation and
                total is not None and total < 0):  # noqa: E501
            raise ValueError("Invalid value for `total`, must be a value greater than or equal to `0`")  # noqa: E501

        self._total = total

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
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

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, OnePageStudyPort):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, OnePageStudyPort):
            return True

        return self.to_dict() != other.to_dict()
