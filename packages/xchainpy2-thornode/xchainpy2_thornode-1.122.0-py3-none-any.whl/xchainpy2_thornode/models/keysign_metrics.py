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

class KeysignMetrics(object):
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
        'tx_id': 'str',
        'node_tss_times': 'list[TssMetric]'
    }

    attribute_map = {
        'tx_id': 'tx_id',
        'node_tss_times': 'node_tss_times'
    }

    def __init__(self, tx_id=None, node_tss_times=None):  # noqa: E501
        """KeysignMetrics - a model defined in Swagger"""  # noqa: E501
        self._tx_id = None
        self._node_tss_times = None
        self.discriminator = None
        if tx_id is not None:
            self.tx_id = tx_id
        if node_tss_times is not None:
            self.node_tss_times = node_tss_times

    @property
    def tx_id(self):
        """Gets the tx_id of this KeysignMetrics.  # noqa: E501


        :return: The tx_id of this KeysignMetrics.  # noqa: E501
        :rtype: str
        """
        return self._tx_id

    @tx_id.setter
    def tx_id(self, tx_id):
        """Sets the tx_id of this KeysignMetrics.


        :param tx_id: The tx_id of this KeysignMetrics.  # noqa: E501
        :type: str
        """

        self._tx_id = tx_id

    @property
    def node_tss_times(self):
        """Gets the node_tss_times of this KeysignMetrics.  # noqa: E501


        :return: The node_tss_times of this KeysignMetrics.  # noqa: E501
        :rtype: list[TssMetric]
        """
        return self._node_tss_times

    @node_tss_times.setter
    def node_tss_times(self, node_tss_times):
        """Sets the node_tss_times of this KeysignMetrics.


        :param node_tss_times: The node_tss_times of this KeysignMetrics.  # noqa: E501
        :type: list[TssMetric]
        """

        self._node_tss_times = node_tss_times

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
        if issubclass(KeysignMetrics, dict):
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
        if not isinstance(other, KeysignMetrics):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
