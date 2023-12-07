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


class FileUploadCompletionBody(object):
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
        'parts': 'list[UploadedPart]'
    }

    attribute_map = {
        'parts': 'parts'
    }

    def __init__(self, parts=None, local_vars_configuration=None):  # noqa: E501
        """FileUploadCompletionBody - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._parts = None
        self.discriminator = None

        self.parts = parts

    @property
    def parts(self):
        """Gets the parts of this FileUploadCompletionBody.  # noqa: E501


        :return: The parts of this FileUploadCompletionBody.  # noqa: E501
        :rtype: list[UploadedPart]
        """
        return self._parts

    @parts.setter
    def parts(self, parts):
        """Sets the parts of this FileUploadCompletionBody.


        :param parts: The parts of this FileUploadCompletionBody.  # noqa: E501
        :type: list[UploadedPart]
        """
        if self.local_vars_configuration.client_side_validation and parts is None:  # noqa: E501
            raise ValueError("Invalid value for `parts`, must not be `None`")  # noqa: E501

        self._parts = parts

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
        if not isinstance(other, FileUploadCompletionBody):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, FileUploadCompletionBody):
            return True

        return self.to_dict() != other.to_dict()
