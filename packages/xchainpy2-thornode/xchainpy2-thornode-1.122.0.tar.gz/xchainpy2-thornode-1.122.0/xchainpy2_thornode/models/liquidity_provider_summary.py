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

class LiquidityProviderSummary(object):
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
        'asset': 'str',
        'rune_address': 'str',
        'asset_address': 'str',
        'last_add_height': 'int',
        'last_withdraw_height': 'int',
        'units': 'str',
        'pending_rune': 'str',
        'pending_asset': 'str',
        'pending_tx_id': 'str',
        'rune_deposit_value': 'str',
        'asset_deposit_value': 'str'
    }

    attribute_map = {
        'asset': 'asset',
        'rune_address': 'rune_address',
        'asset_address': 'asset_address',
        'last_add_height': 'last_add_height',
        'last_withdraw_height': 'last_withdraw_height',
        'units': 'units',
        'pending_rune': 'pending_rune',
        'pending_asset': 'pending_asset',
        'pending_tx_id': 'pending_tx_id',
        'rune_deposit_value': 'rune_deposit_value',
        'asset_deposit_value': 'asset_deposit_value'
    }

    def __init__(self, asset=None, rune_address=None, asset_address=None, last_add_height=None, last_withdraw_height=None, units=None, pending_rune=None, pending_asset=None, pending_tx_id=None, rune_deposit_value=None, asset_deposit_value=None):  # noqa: E501
        """LiquidityProviderSummary - a model defined in Swagger"""  # noqa: E501
        self._asset = None
        self._rune_address = None
        self._asset_address = None
        self._last_add_height = None
        self._last_withdraw_height = None
        self._units = None
        self._pending_rune = None
        self._pending_asset = None
        self._pending_tx_id = None
        self._rune_deposit_value = None
        self._asset_deposit_value = None
        self.discriminator = None
        self.asset = asset
        if rune_address is not None:
            self.rune_address = rune_address
        if asset_address is not None:
            self.asset_address = asset_address
        if last_add_height is not None:
            self.last_add_height = last_add_height
        if last_withdraw_height is not None:
            self.last_withdraw_height = last_withdraw_height
        self.units = units
        self.pending_rune = pending_rune
        self.pending_asset = pending_asset
        if pending_tx_id is not None:
            self.pending_tx_id = pending_tx_id
        self.rune_deposit_value = rune_deposit_value
        self.asset_deposit_value = asset_deposit_value

    @property
    def asset(self):
        """Gets the asset of this LiquidityProviderSummary.  # noqa: E501


        :return: The asset of this LiquidityProviderSummary.  # noqa: E501
        :rtype: str
        """
        return self._asset

    @asset.setter
    def asset(self, asset):
        """Sets the asset of this LiquidityProviderSummary.


        :param asset: The asset of this LiquidityProviderSummary.  # noqa: E501
        :type: str
        """
        if asset is None:
            raise ValueError("Invalid value for `asset`, must not be `None`")  # noqa: E501

        self._asset = asset

    @property
    def rune_address(self):
        """Gets the rune_address of this LiquidityProviderSummary.  # noqa: E501


        :return: The rune_address of this LiquidityProviderSummary.  # noqa: E501
        :rtype: str
        """
        return self._rune_address

    @rune_address.setter
    def rune_address(self, rune_address):
        """Sets the rune_address of this LiquidityProviderSummary.


        :param rune_address: The rune_address of this LiquidityProviderSummary.  # noqa: E501
        :type: str
        """

        self._rune_address = rune_address

    @property
    def asset_address(self):
        """Gets the asset_address of this LiquidityProviderSummary.  # noqa: E501


        :return: The asset_address of this LiquidityProviderSummary.  # noqa: E501
        :rtype: str
        """
        return self._asset_address

    @asset_address.setter
    def asset_address(self, asset_address):
        """Sets the asset_address of this LiquidityProviderSummary.


        :param asset_address: The asset_address of this LiquidityProviderSummary.  # noqa: E501
        :type: str
        """

        self._asset_address = asset_address

    @property
    def last_add_height(self):
        """Gets the last_add_height of this LiquidityProviderSummary.  # noqa: E501


        :return: The last_add_height of this LiquidityProviderSummary.  # noqa: E501
        :rtype: int
        """
        return self._last_add_height

    @last_add_height.setter
    def last_add_height(self, last_add_height):
        """Sets the last_add_height of this LiquidityProviderSummary.


        :param last_add_height: The last_add_height of this LiquidityProviderSummary.  # noqa: E501
        :type: int
        """

        self._last_add_height = last_add_height

    @property
    def last_withdraw_height(self):
        """Gets the last_withdraw_height of this LiquidityProviderSummary.  # noqa: E501


        :return: The last_withdraw_height of this LiquidityProviderSummary.  # noqa: E501
        :rtype: int
        """
        return self._last_withdraw_height

    @last_withdraw_height.setter
    def last_withdraw_height(self, last_withdraw_height):
        """Sets the last_withdraw_height of this LiquidityProviderSummary.


        :param last_withdraw_height: The last_withdraw_height of this LiquidityProviderSummary.  # noqa: E501
        :type: int
        """

        self._last_withdraw_height = last_withdraw_height

    @property
    def units(self):
        """Gets the units of this LiquidityProviderSummary.  # noqa: E501


        :return: The units of this LiquidityProviderSummary.  # noqa: E501
        :rtype: str
        """
        return self._units

    @units.setter
    def units(self, units):
        """Sets the units of this LiquidityProviderSummary.


        :param units: The units of this LiquidityProviderSummary.  # noqa: E501
        :type: str
        """
        if units is None:
            raise ValueError("Invalid value for `units`, must not be `None`")  # noqa: E501

        self._units = units

    @property
    def pending_rune(self):
        """Gets the pending_rune of this LiquidityProviderSummary.  # noqa: E501


        :return: The pending_rune of this LiquidityProviderSummary.  # noqa: E501
        :rtype: str
        """
        return self._pending_rune

    @pending_rune.setter
    def pending_rune(self, pending_rune):
        """Sets the pending_rune of this LiquidityProviderSummary.


        :param pending_rune: The pending_rune of this LiquidityProviderSummary.  # noqa: E501
        :type: str
        """
        if pending_rune is None:
            raise ValueError("Invalid value for `pending_rune`, must not be `None`")  # noqa: E501

        self._pending_rune = pending_rune

    @property
    def pending_asset(self):
        """Gets the pending_asset of this LiquidityProviderSummary.  # noqa: E501


        :return: The pending_asset of this LiquidityProviderSummary.  # noqa: E501
        :rtype: str
        """
        return self._pending_asset

    @pending_asset.setter
    def pending_asset(self, pending_asset):
        """Sets the pending_asset of this LiquidityProviderSummary.


        :param pending_asset: The pending_asset of this LiquidityProviderSummary.  # noqa: E501
        :type: str
        """
        if pending_asset is None:
            raise ValueError("Invalid value for `pending_asset`, must not be `None`")  # noqa: E501

        self._pending_asset = pending_asset

    @property
    def pending_tx_id(self):
        """Gets the pending_tx_id of this LiquidityProviderSummary.  # noqa: E501


        :return: The pending_tx_id of this LiquidityProviderSummary.  # noqa: E501
        :rtype: str
        """
        return self._pending_tx_id

    @pending_tx_id.setter
    def pending_tx_id(self, pending_tx_id):
        """Sets the pending_tx_id of this LiquidityProviderSummary.


        :param pending_tx_id: The pending_tx_id of this LiquidityProviderSummary.  # noqa: E501
        :type: str
        """

        self._pending_tx_id = pending_tx_id

    @property
    def rune_deposit_value(self):
        """Gets the rune_deposit_value of this LiquidityProviderSummary.  # noqa: E501


        :return: The rune_deposit_value of this LiquidityProviderSummary.  # noqa: E501
        :rtype: str
        """
        return self._rune_deposit_value

    @rune_deposit_value.setter
    def rune_deposit_value(self, rune_deposit_value):
        """Sets the rune_deposit_value of this LiquidityProviderSummary.


        :param rune_deposit_value: The rune_deposit_value of this LiquidityProviderSummary.  # noqa: E501
        :type: str
        """
        if rune_deposit_value is None:
            raise ValueError("Invalid value for `rune_deposit_value`, must not be `None`")  # noqa: E501

        self._rune_deposit_value = rune_deposit_value

    @property
    def asset_deposit_value(self):
        """Gets the asset_deposit_value of this LiquidityProviderSummary.  # noqa: E501


        :return: The asset_deposit_value of this LiquidityProviderSummary.  # noqa: E501
        :rtype: str
        """
        return self._asset_deposit_value

    @asset_deposit_value.setter
    def asset_deposit_value(self, asset_deposit_value):
        """Sets the asset_deposit_value of this LiquidityProviderSummary.


        :param asset_deposit_value: The asset_deposit_value of this LiquidityProviderSummary.  # noqa: E501
        :type: str
        """
        if asset_deposit_value is None:
            raise ValueError("Invalid value for `asset_deposit_value`, must not be `None`")  # noqa: E501

        self._asset_deposit_value = asset_deposit_value

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
        if issubclass(LiquidityProviderSummary, dict):
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
        if not isinstance(other, LiquidityProviderSummary):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
