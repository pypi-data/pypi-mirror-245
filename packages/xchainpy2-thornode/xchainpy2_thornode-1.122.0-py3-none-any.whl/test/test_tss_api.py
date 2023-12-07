# coding: utf-8

"""
    Thornode API

    Thornode REST API.  # noqa: E501

    OpenAPI spec version: 1.122.0
    Contact: devs@thorchain.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import unittest

import xchainpy2_thornode
from xchainpy2_thornode.api.tss_api import TSSApi  # noqa: E501
from xchainpy2_thornode.rest import ApiException


class TestTSSApi(unittest.TestCase):
    """TSSApi unit test stubs"""

    def setUp(self):
        self.api = TSSApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_keysign(self):
        """Test case for keysign

        """
        pass

    def test_keysign_pubkey(self):
        """Test case for keysign_pubkey

        """
        pass

    def test_metrics(self):
        """Test case for metrics

        """
        pass

    def test_metrics_keygen(self):
        """Test case for metrics_keygen

        """
        pass


if __name__ == '__main__':
    unittest.main()
