# coding: utf-8

"""
    Mayanode API

    Mayanode REST API.  # noqa: E501

    OpenAPI spec version: 1.107.1
    Contact: devs@mayachain.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class QuoteSaverDepositResponse(object):
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
        'inbound_address': 'str',
        'memo': 'str',
        'expected_amount_out': 'str',
        'inbound_confirmation_blocks': 'int',
        'inbound_confirmation_seconds': 'int',
        'fees': 'QuoteFees',
        'slippage_bps': 'int'
    }

    attribute_map = {
        'inbound_address': 'inbound_address',
        'memo': 'memo',
        'expected_amount_out': 'expected_amount_out',
        'inbound_confirmation_blocks': 'inbound_confirmation_blocks',
        'inbound_confirmation_seconds': 'inbound_confirmation_seconds',
        'fees': 'fees',
        'slippage_bps': 'slippage_bps'
    }

    def __init__(self, inbound_address=None, memo=None, expected_amount_out=None, inbound_confirmation_blocks=None, inbound_confirmation_seconds=None, fees=None, slippage_bps=None):  # noqa: E501
        """QuoteSaverDepositResponse - a model defined in Swagger"""  # noqa: E501
        self._inbound_address = None
        self._memo = None
        self._expected_amount_out = None
        self._inbound_confirmation_blocks = None
        self._inbound_confirmation_seconds = None
        self._fees = None
        self._slippage_bps = None
        self.discriminator = None
        self.inbound_address = inbound_address
        self.memo = memo
        self.expected_amount_out = expected_amount_out
        if inbound_confirmation_blocks is not None:
            self.inbound_confirmation_blocks = inbound_confirmation_blocks
        if inbound_confirmation_seconds is not None:
            self.inbound_confirmation_seconds = inbound_confirmation_seconds
        self.fees = fees
        self.slippage_bps = slippage_bps

    @property
    def inbound_address(self):
        """Gets the inbound_address of this QuoteSaverDepositResponse.  # noqa: E501

        the inbound address for the transaction on the source chain  # noqa: E501

        :return: The inbound_address of this QuoteSaverDepositResponse.  # noqa: E501
        :rtype: str
        """
        return self._inbound_address

    @inbound_address.setter
    def inbound_address(self, inbound_address):
        """Sets the inbound_address of this QuoteSaverDepositResponse.

        the inbound address for the transaction on the source chain  # noqa: E501

        :param inbound_address: The inbound_address of this QuoteSaverDepositResponse.  # noqa: E501
        :type: str
        """
        if inbound_address is None:
            raise ValueError("Invalid value for `inbound_address`, must not be `None`")  # noqa: E501

        self._inbound_address = inbound_address

    @property
    def memo(self):
        """Gets the memo of this QuoteSaverDepositResponse.  # noqa: E501

        generated memo for the deposit  # noqa: E501

        :return: The memo of this QuoteSaverDepositResponse.  # noqa: E501
        :rtype: str
        """
        return self._memo

    @memo.setter
    def memo(self, memo):
        """Sets the memo of this QuoteSaverDepositResponse.

        generated memo for the deposit  # noqa: E501

        :param memo: The memo of this QuoteSaverDepositResponse.  # noqa: E501
        :type: str
        """
        if memo is None:
            raise ValueError("Invalid value for `memo`, must not be `None`")  # noqa: E501

        self._memo = memo

    @property
    def expected_amount_out(self):
        """Gets the expected_amount_out of this QuoteSaverDepositResponse.  # noqa: E501

        the minimum amount of the target asset the user can expect to deposit after fees  # noqa: E501

        :return: The expected_amount_out of this QuoteSaverDepositResponse.  # noqa: E501
        :rtype: str
        """
        return self._expected_amount_out

    @expected_amount_out.setter
    def expected_amount_out(self, expected_amount_out):
        """Sets the expected_amount_out of this QuoteSaverDepositResponse.

        the minimum amount of the target asset the user can expect to deposit after fees  # noqa: E501

        :param expected_amount_out: The expected_amount_out of this QuoteSaverDepositResponse.  # noqa: E501
        :type: str
        """
        if expected_amount_out is None:
            raise ValueError("Invalid value for `expected_amount_out`, must not be `None`")  # noqa: E501

        self._expected_amount_out = expected_amount_out

    @property
    def inbound_confirmation_blocks(self):
        """Gets the inbound_confirmation_blocks of this QuoteSaverDepositResponse.  # noqa: E501

        the approximate number of source chain blocks required before processing  # noqa: E501

        :return: The inbound_confirmation_blocks of this QuoteSaverDepositResponse.  # noqa: E501
        :rtype: int
        """
        return self._inbound_confirmation_blocks

    @inbound_confirmation_blocks.setter
    def inbound_confirmation_blocks(self, inbound_confirmation_blocks):
        """Sets the inbound_confirmation_blocks of this QuoteSaverDepositResponse.

        the approximate number of source chain blocks required before processing  # noqa: E501

        :param inbound_confirmation_blocks: The inbound_confirmation_blocks of this QuoteSaverDepositResponse.  # noqa: E501
        :type: int
        """

        self._inbound_confirmation_blocks = inbound_confirmation_blocks

    @property
    def inbound_confirmation_seconds(self):
        """Gets the inbound_confirmation_seconds of this QuoteSaverDepositResponse.  # noqa: E501

        the approximate seconds for block confirmations required before processing  # noqa: E501

        :return: The inbound_confirmation_seconds of this QuoteSaverDepositResponse.  # noqa: E501
        :rtype: int
        """
        return self._inbound_confirmation_seconds

    @inbound_confirmation_seconds.setter
    def inbound_confirmation_seconds(self, inbound_confirmation_seconds):
        """Sets the inbound_confirmation_seconds of this QuoteSaverDepositResponse.

        the approximate seconds for block confirmations required before processing  # noqa: E501

        :param inbound_confirmation_seconds: The inbound_confirmation_seconds of this QuoteSaverDepositResponse.  # noqa: E501
        :type: int
        """

        self._inbound_confirmation_seconds = inbound_confirmation_seconds

    @property
    def fees(self):
        """Gets the fees of this QuoteSaverDepositResponse.  # noqa: E501


        :return: The fees of this QuoteSaverDepositResponse.  # noqa: E501
        :rtype: QuoteFees
        """
        return self._fees

    @fees.setter
    def fees(self, fees):
        """Sets the fees of this QuoteSaverDepositResponse.


        :param fees: The fees of this QuoteSaverDepositResponse.  # noqa: E501
        :type: QuoteFees
        """
        if fees is None:
            raise ValueError("Invalid value for `fees`, must not be `None`")  # noqa: E501

        self._fees = fees

    @property
    def slippage_bps(self):
        """Gets the slippage_bps of this QuoteSaverDepositResponse.  # noqa: E501

        the swap slippage in basis points  # noqa: E501

        :return: The slippage_bps of this QuoteSaverDepositResponse.  # noqa: E501
        :rtype: int
        """
        return self._slippage_bps

    @slippage_bps.setter
    def slippage_bps(self, slippage_bps):
        """Sets the slippage_bps of this QuoteSaverDepositResponse.

        the swap slippage in basis points  # noqa: E501

        :param slippage_bps: The slippage_bps of this QuoteSaverDepositResponse.  # noqa: E501
        :type: int
        """
        if slippage_bps is None:
            raise ValueError("Invalid value for `slippage_bps`, must not be `None`")  # noqa: E501

        self._slippage_bps = slippage_bps

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
        if issubclass(QuoteSaverDepositResponse, dict):
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
        if not isinstance(other, QuoteSaverDepositResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
