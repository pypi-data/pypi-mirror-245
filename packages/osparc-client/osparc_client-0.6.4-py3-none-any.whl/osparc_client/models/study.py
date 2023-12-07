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


class Study(object):
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
        'uid': 'str',
        'title': 'str',
        'description': 'str'
    }

    attribute_map = {
        'uid': 'uid',
        'title': 'title',
        'description': 'description'
    }

    def __init__(self, uid=None, title=None, description=None, local_vars_configuration=None):  # noqa: E501
        """Study - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._uid = None
        self._title = None
        self._description = None
        self.discriminator = None

        self.uid = uid
        if title is not None:
            self.title = title
        if description is not None:
            self.description = description

    @property
    def uid(self):
        """Gets the uid of this Study.  # noqa: E501


        :return: The uid of this Study.  # noqa: E501
        :rtype: str
        """
        return self._uid

    @uid.setter
    def uid(self, uid):
        """Sets the uid of this Study.


        :param uid: The uid of this Study.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and uid is None:  # noqa: E501
            raise ValueError("Invalid value for `uid`, must not be `None`")  # noqa: E501

        self._uid = uid

    @property
    def title(self):
        """Gets the title of this Study.  # noqa: E501


        :return: The title of this Study.  # noqa: E501
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title):
        """Sets the title of this Study.


        :param title: The title of this Study.  # noqa: E501
        :type: str
        """

        self._title = title

    @property
    def description(self):
        """Gets the description of this Study.  # noqa: E501


        :return: The description of this Study.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this Study.


        :param description: The description of this Study.  # noqa: E501
        :type: str
        """

        self._description = description

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
        if not isinstance(other, Study):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, Study):
            return True

        return self.to_dict() != other.to_dict()
