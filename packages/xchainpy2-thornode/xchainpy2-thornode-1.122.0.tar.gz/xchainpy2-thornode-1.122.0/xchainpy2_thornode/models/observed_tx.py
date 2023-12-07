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

class ObservedTx(object):
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
        'tx': 'Tx',
        'observed_pub_key': 'str',
        'external_observed_height': 'int',
        'external_confirmation_delay_height': 'int',
        'aggregator': 'str',
        'aggregator_target': 'str',
        'aggregator_target_limit': 'str',
        'signers': 'list[str]',
        'keysign_ms': 'int',
        'out_hashes': 'list[str]',
        'status': 'str'
    }

    attribute_map = {
        'tx': 'tx',
        'observed_pub_key': 'observed_pub_key',
        'external_observed_height': 'external_observed_height',
        'external_confirmation_delay_height': 'external_confirmation_delay_height',
        'aggregator': 'aggregator',
        'aggregator_target': 'aggregator_target',
        'aggregator_target_limit': 'aggregator_target_limit',
        'signers': 'signers',
        'keysign_ms': 'keysign_ms',
        'out_hashes': 'out_hashes',
        'status': 'status'
    }

    def __init__(self, tx=None, observed_pub_key=None, external_observed_height=None, external_confirmation_delay_height=None, aggregator=None, aggregator_target=None, aggregator_target_limit=None, signers=None, keysign_ms=None, out_hashes=None, status=None):  # noqa: E501
        """ObservedTx - a model defined in Swagger"""  # noqa: E501
        self._tx = None
        self._observed_pub_key = None
        self._external_observed_height = None
        self._external_confirmation_delay_height = None
        self._aggregator = None
        self._aggregator_target = None
        self._aggregator_target_limit = None
        self._signers = None
        self._keysign_ms = None
        self._out_hashes = None
        self._status = None
        self.discriminator = None
        self.tx = tx
        if observed_pub_key is not None:
            self.observed_pub_key = observed_pub_key
        if external_observed_height is not None:
            self.external_observed_height = external_observed_height
        if external_confirmation_delay_height is not None:
            self.external_confirmation_delay_height = external_confirmation_delay_height
        if aggregator is not None:
            self.aggregator = aggregator
        if aggregator_target is not None:
            self.aggregator_target = aggregator_target
        if aggregator_target_limit is not None:
            self.aggregator_target_limit = aggregator_target_limit
        if signers is not None:
            self.signers = signers
        if keysign_ms is not None:
            self.keysign_ms = keysign_ms
        if out_hashes is not None:
            self.out_hashes = out_hashes
        if status is not None:
            self.status = status

    @property
    def tx(self):
        """Gets the tx of this ObservedTx.  # noqa: E501


        :return: The tx of this ObservedTx.  # noqa: E501
        :rtype: Tx
        """
        return self._tx

    @tx.setter
    def tx(self, tx):
        """Sets the tx of this ObservedTx.


        :param tx: The tx of this ObservedTx.  # noqa: E501
        :type: Tx
        """
        if tx is None:
            raise ValueError("Invalid value for `tx`, must not be `None`")  # noqa: E501

        self._tx = tx

    @property
    def observed_pub_key(self):
        """Gets the observed_pub_key of this ObservedTx.  # noqa: E501


        :return: The observed_pub_key of this ObservedTx.  # noqa: E501
        :rtype: str
        """
        return self._observed_pub_key

    @observed_pub_key.setter
    def observed_pub_key(self, observed_pub_key):
        """Sets the observed_pub_key of this ObservedTx.


        :param observed_pub_key: The observed_pub_key of this ObservedTx.  # noqa: E501
        :type: str
        """

        self._observed_pub_key = observed_pub_key

    @property
    def external_observed_height(self):
        """Gets the external_observed_height of this ObservedTx.  # noqa: E501

        the block height on the external source chain when the transaction was observed, not provided if chain is THOR  # noqa: E501

        :return: The external_observed_height of this ObservedTx.  # noqa: E501
        :rtype: int
        """
        return self._external_observed_height

    @external_observed_height.setter
    def external_observed_height(self, external_observed_height):
        """Sets the external_observed_height of this ObservedTx.

        the block height on the external source chain when the transaction was observed, not provided if chain is THOR  # noqa: E501

        :param external_observed_height: The external_observed_height of this ObservedTx.  # noqa: E501
        :type: int
        """

        self._external_observed_height = external_observed_height

    @property
    def external_confirmation_delay_height(self):
        """Gets the external_confirmation_delay_height of this ObservedTx.  # noqa: E501

        the block height on the external source chain when confirmation counting will be complete, not provided if chain is THOR  # noqa: E501

        :return: The external_confirmation_delay_height of this ObservedTx.  # noqa: E501
        :rtype: int
        """
        return self._external_confirmation_delay_height

    @external_confirmation_delay_height.setter
    def external_confirmation_delay_height(self, external_confirmation_delay_height):
        """Sets the external_confirmation_delay_height of this ObservedTx.

        the block height on the external source chain when confirmation counting will be complete, not provided if chain is THOR  # noqa: E501

        :param external_confirmation_delay_height: The external_confirmation_delay_height of this ObservedTx.  # noqa: E501
        :type: int
        """

        self._external_confirmation_delay_height = external_confirmation_delay_height

    @property
    def aggregator(self):
        """Gets the aggregator of this ObservedTx.  # noqa: E501

        the outbound aggregator to use, will also match a suffix  # noqa: E501

        :return: The aggregator of this ObservedTx.  # noqa: E501
        :rtype: str
        """
        return self._aggregator

    @aggregator.setter
    def aggregator(self, aggregator):
        """Sets the aggregator of this ObservedTx.

        the outbound aggregator to use, will also match a suffix  # noqa: E501

        :param aggregator: The aggregator of this ObservedTx.  # noqa: E501
        :type: str
        """

        self._aggregator = aggregator

    @property
    def aggregator_target(self):
        """Gets the aggregator_target of this ObservedTx.  # noqa: E501

        the aggregator target asset provided to transferOutAndCall  # noqa: E501

        :return: The aggregator_target of this ObservedTx.  # noqa: E501
        :rtype: str
        """
        return self._aggregator_target

    @aggregator_target.setter
    def aggregator_target(self, aggregator_target):
        """Sets the aggregator_target of this ObservedTx.

        the aggregator target asset provided to transferOutAndCall  # noqa: E501

        :param aggregator_target: The aggregator_target of this ObservedTx.  # noqa: E501
        :type: str
        """

        self._aggregator_target = aggregator_target

    @property
    def aggregator_target_limit(self):
        """Gets the aggregator_target_limit of this ObservedTx.  # noqa: E501

        the aggregator target asset limit provided to transferOutAndCall  # noqa: E501

        :return: The aggregator_target_limit of this ObservedTx.  # noqa: E501
        :rtype: str
        """
        return self._aggregator_target_limit

    @aggregator_target_limit.setter
    def aggregator_target_limit(self, aggregator_target_limit):
        """Sets the aggregator_target_limit of this ObservedTx.

        the aggregator target asset limit provided to transferOutAndCall  # noqa: E501

        :param aggregator_target_limit: The aggregator_target_limit of this ObservedTx.  # noqa: E501
        :type: str
        """

        self._aggregator_target_limit = aggregator_target_limit

    @property
    def signers(self):
        """Gets the signers of this ObservedTx.  # noqa: E501


        :return: The signers of this ObservedTx.  # noqa: E501
        :rtype: list[str]
        """
        return self._signers

    @signers.setter
    def signers(self, signers):
        """Sets the signers of this ObservedTx.


        :param signers: The signers of this ObservedTx.  # noqa: E501
        :type: list[str]
        """

        self._signers = signers

    @property
    def keysign_ms(self):
        """Gets the keysign_ms of this ObservedTx.  # noqa: E501


        :return: The keysign_ms of this ObservedTx.  # noqa: E501
        :rtype: int
        """
        return self._keysign_ms

    @keysign_ms.setter
    def keysign_ms(self, keysign_ms):
        """Sets the keysign_ms of this ObservedTx.


        :param keysign_ms: The keysign_ms of this ObservedTx.  # noqa: E501
        :type: int
        """

        self._keysign_ms = keysign_ms

    @property
    def out_hashes(self):
        """Gets the out_hashes of this ObservedTx.  # noqa: E501


        :return: The out_hashes of this ObservedTx.  # noqa: E501
        :rtype: list[str]
        """
        return self._out_hashes

    @out_hashes.setter
    def out_hashes(self, out_hashes):
        """Sets the out_hashes of this ObservedTx.


        :param out_hashes: The out_hashes of this ObservedTx.  # noqa: E501
        :type: list[str]
        """

        self._out_hashes = out_hashes

    @property
    def status(self):
        """Gets the status of this ObservedTx.  # noqa: E501


        :return: The status of this ObservedTx.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this ObservedTx.


        :param status: The status of this ObservedTx.  # noqa: E501
        :type: str
        """
        allowed_values = ["done", "incomplete"]  # noqa: E501
        if status not in allowed_values:
            raise ValueError(
                "Invalid value for `status` ({0}), must be one of {1}"  # noqa: E501
                .format(status, allowed_values)
            )

        self._status = status

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
        if issubclass(ObservedTx, dict):
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
        if not isinstance(other, ObservedTx):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
