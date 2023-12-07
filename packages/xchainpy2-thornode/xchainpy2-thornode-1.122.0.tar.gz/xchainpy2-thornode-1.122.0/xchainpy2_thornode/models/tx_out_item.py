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

class TxOutItem(object):
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
        'chain': 'str',
        'to_address': 'str',
        'vault_pub_key': 'str',
        'coin': 'Coin',
        'memo': 'str',
        'max_gas': 'list[Coin]',
        'gas_rate': 'int',
        'in_hash': 'str',
        'out_hash': 'str',
        'height': 'int'
    }

    attribute_map = {
        'chain': 'chain',
        'to_address': 'to_address',
        'vault_pub_key': 'vault_pub_key',
        'coin': 'coin',
        'memo': 'memo',
        'max_gas': 'max_gas',
        'gas_rate': 'gas_rate',
        'in_hash': 'in_hash',
        'out_hash': 'out_hash',
        'height': 'height'
    }

    def __init__(self, chain=None, to_address=None, vault_pub_key=None, coin=None, memo=None, max_gas=None, gas_rate=None, in_hash=None, out_hash=None, height=None):  # noqa: E501
        """TxOutItem - a model defined in Swagger"""  # noqa: E501
        self._chain = None
        self._to_address = None
        self._vault_pub_key = None
        self._coin = None
        self._memo = None
        self._max_gas = None
        self._gas_rate = None
        self._in_hash = None
        self._out_hash = None
        self._height = None
        self.discriminator = None
        self.chain = chain
        self.to_address = to_address
        if vault_pub_key is not None:
            self.vault_pub_key = vault_pub_key
        self.coin = coin
        if memo is not None:
            self.memo = memo
        self.max_gas = max_gas
        if gas_rate is not None:
            self.gas_rate = gas_rate
        if in_hash is not None:
            self.in_hash = in_hash
        if out_hash is not None:
            self.out_hash = out_hash
        self.height = height

    @property
    def chain(self):
        """Gets the chain of this TxOutItem.  # noqa: E501


        :return: The chain of this TxOutItem.  # noqa: E501
        :rtype: str
        """
        return self._chain

    @chain.setter
    def chain(self, chain):
        """Sets the chain of this TxOutItem.


        :param chain: The chain of this TxOutItem.  # noqa: E501
        :type: str
        """
        if chain is None:
            raise ValueError("Invalid value for `chain`, must not be `None`")  # noqa: E501

        self._chain = chain

    @property
    def to_address(self):
        """Gets the to_address of this TxOutItem.  # noqa: E501


        :return: The to_address of this TxOutItem.  # noqa: E501
        :rtype: str
        """
        return self._to_address

    @to_address.setter
    def to_address(self, to_address):
        """Sets the to_address of this TxOutItem.


        :param to_address: The to_address of this TxOutItem.  # noqa: E501
        :type: str
        """
        if to_address is None:
            raise ValueError("Invalid value for `to_address`, must not be `None`")  # noqa: E501

        self._to_address = to_address

    @property
    def vault_pub_key(self):
        """Gets the vault_pub_key of this TxOutItem.  # noqa: E501


        :return: The vault_pub_key of this TxOutItem.  # noqa: E501
        :rtype: str
        """
        return self._vault_pub_key

    @vault_pub_key.setter
    def vault_pub_key(self, vault_pub_key):
        """Sets the vault_pub_key of this TxOutItem.


        :param vault_pub_key: The vault_pub_key of this TxOutItem.  # noqa: E501
        :type: str
        """

        self._vault_pub_key = vault_pub_key

    @property
    def coin(self):
        """Gets the coin of this TxOutItem.  # noqa: E501


        :return: The coin of this TxOutItem.  # noqa: E501
        :rtype: Coin
        """
        return self._coin

    @coin.setter
    def coin(self, coin):
        """Sets the coin of this TxOutItem.


        :param coin: The coin of this TxOutItem.  # noqa: E501
        :type: Coin
        """
        if coin is None:
            raise ValueError("Invalid value for `coin`, must not be `None`")  # noqa: E501

        self._coin = coin

    @property
    def memo(self):
        """Gets the memo of this TxOutItem.  # noqa: E501


        :return: The memo of this TxOutItem.  # noqa: E501
        :rtype: str
        """
        return self._memo

    @memo.setter
    def memo(self, memo):
        """Sets the memo of this TxOutItem.


        :param memo: The memo of this TxOutItem.  # noqa: E501
        :type: str
        """

        self._memo = memo

    @property
    def max_gas(self):
        """Gets the max_gas of this TxOutItem.  # noqa: E501


        :return: The max_gas of this TxOutItem.  # noqa: E501
        :rtype: list[Coin]
        """
        return self._max_gas

    @max_gas.setter
    def max_gas(self, max_gas):
        """Sets the max_gas of this TxOutItem.


        :param max_gas: The max_gas of this TxOutItem.  # noqa: E501
        :type: list[Coin]
        """
        if max_gas is None:
            raise ValueError("Invalid value for `max_gas`, must not be `None`")  # noqa: E501

        self._max_gas = max_gas

    @property
    def gas_rate(self):
        """Gets the gas_rate of this TxOutItem.  # noqa: E501


        :return: The gas_rate of this TxOutItem.  # noqa: E501
        :rtype: int
        """
        return self._gas_rate

    @gas_rate.setter
    def gas_rate(self, gas_rate):
        """Sets the gas_rate of this TxOutItem.


        :param gas_rate: The gas_rate of this TxOutItem.  # noqa: E501
        :type: int
        """

        self._gas_rate = gas_rate

    @property
    def in_hash(self):
        """Gets the in_hash of this TxOutItem.  # noqa: E501


        :return: The in_hash of this TxOutItem.  # noqa: E501
        :rtype: str
        """
        return self._in_hash

    @in_hash.setter
    def in_hash(self, in_hash):
        """Sets the in_hash of this TxOutItem.


        :param in_hash: The in_hash of this TxOutItem.  # noqa: E501
        :type: str
        """

        self._in_hash = in_hash

    @property
    def out_hash(self):
        """Gets the out_hash of this TxOutItem.  # noqa: E501


        :return: The out_hash of this TxOutItem.  # noqa: E501
        :rtype: str
        """
        return self._out_hash

    @out_hash.setter
    def out_hash(self, out_hash):
        """Sets the out_hash of this TxOutItem.


        :param out_hash: The out_hash of this TxOutItem.  # noqa: E501
        :type: str
        """

        self._out_hash = out_hash

    @property
    def height(self):
        """Gets the height of this TxOutItem.  # noqa: E501


        :return: The height of this TxOutItem.  # noqa: E501
        :rtype: int
        """
        return self._height

    @height.setter
    def height(self, height):
        """Sets the height of this TxOutItem.


        :param height: The height of this TxOutItem.  # noqa: E501
        :type: int
        """
        if height is None:
            raise ValueError("Invalid value for `height`, must not be `None`")  # noqa: E501

        self._height = height

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
        if issubclass(TxOutItem, dict):
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
        if not isinstance(other, TxOutItem):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
