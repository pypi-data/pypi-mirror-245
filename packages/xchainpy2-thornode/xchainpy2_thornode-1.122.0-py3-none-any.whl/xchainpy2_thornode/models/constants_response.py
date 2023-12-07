# coding: utf-8

"""
    Thornode API

    Thornode REST API.  # noqa: E501

    OpenAPI spec version: 1.122.0
    Contact: devs@thorchain.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class ConstantsResponse(object):
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
        'int_64_values': 'dict(str, str)',
        'bool_values': 'dict(str, str)',
        'string_values': 'dict(str, str)'
    }

    attribute_map = {
        'int_64_values': 'int_64_values',
        'bool_values': 'bool_values',
        'string_values': 'string_values'
    }

    def __init__(self, int_64_values=None, bool_values=None, string_values=None):  # noqa: E501
        """ConstantsResponse - a model defined in Swagger"""  # noqa: E501
        self._int_64_values = None
        self._bool_values = None
        self._string_values = None
        self.discriminator = None
        if int_64_values is not None:
            self.int_64_values = int_64_values
        if bool_values is not None:
            self.bool_values = bool_values
        if string_values is not None:
            self.string_values = string_values

    @property
    def int_64_values(self):
        """Gets the int_64_values of this ConstantsResponse.  # noqa: E501


        :return: The int_64_values of this ConstantsResponse.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._int_64_values

    @int_64_values.setter
    def int_64_values(self, int_64_values):
        """Sets the int_64_values of this ConstantsResponse.


        :param int_64_values: The int_64_values of this ConstantsResponse.  # noqa: E501
        :type: dict(str, str)
        """

        self._int_64_values = int_64_values

    @property
    def bool_values(self):
        """Gets the bool_values of this ConstantsResponse.  # noqa: E501


        :return: The bool_values of this ConstantsResponse.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._bool_values

    @bool_values.setter
    def bool_values(self, bool_values):
        """Sets the bool_values of this ConstantsResponse.


        :param bool_values: The bool_values of this ConstantsResponse.  # noqa: E501
        :type: dict(str, str)
        """

        self._bool_values = bool_values

    @property
    def string_values(self):
        """Gets the string_values of this ConstantsResponse.  # noqa: E501


        :return: The string_values of this ConstantsResponse.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._string_values

    @string_values.setter
    def string_values(self, string_values):
        """Sets the string_values of this ConstantsResponse.


        :param string_values: The string_values of this ConstantsResponse.  # noqa: E501
        :type: dict(str, str)
        """

        self._string_values = string_values

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
        if issubclass(ConstantsResponse, dict):
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
        if not isinstance(other, ConstantsResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
