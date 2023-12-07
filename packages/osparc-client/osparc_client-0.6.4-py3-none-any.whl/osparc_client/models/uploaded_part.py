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


class UploadedPart(object):
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
        'number': 'int',
        'e_tag': 'str'
    }

    attribute_map = {
        'number': 'number',
        'e_tag': 'e_tag'
    }

    def __init__(self, number=None, e_tag=None, local_vars_configuration=None):  # noqa: E501
        """UploadedPart - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._number = None
        self._e_tag = None
        self.discriminator = None

        self.number = number
        self.e_tag = e_tag

    @property
    def number(self):
        """Gets the number of this UploadedPart.  # noqa: E501


        :return: The number of this UploadedPart.  # noqa: E501
        :rtype: int
        """
        return self._number

    @number.setter
    def number(self, number):
        """Sets the number of this UploadedPart.


        :param number: The number of this UploadedPart.  # noqa: E501
        :type: int
        """
        if self.local_vars_configuration.client_side_validation and number is None:  # noqa: E501
            raise ValueError("Invalid value for `number`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                number is not None and number <= 0):  # noqa: E501
            raise ValueError("Invalid value for `number`, must be a value greater than `0`")  # noqa: E501

        self._number = number

    @property
    def e_tag(self):
        """Gets the e_tag of this UploadedPart.  # noqa: E501


        :return: The e_tag of this UploadedPart.  # noqa: E501
        :rtype: str
        """
        return self._e_tag

    @e_tag.setter
    def e_tag(self, e_tag):
        """Sets the e_tag of this UploadedPart.


        :param e_tag: The e_tag of this UploadedPart.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and e_tag is None:  # noqa: E501
            raise ValueError("Invalid value for `e_tag`, must not be `None`")  # noqa: E501

        self._e_tag = e_tag

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
        if not isinstance(other, UploadedPart):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, UploadedPart):
            return True

        return self.to_dict() != other.to_dict()
