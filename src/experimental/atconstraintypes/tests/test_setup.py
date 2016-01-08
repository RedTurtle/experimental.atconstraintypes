# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from experimental.atconstraintypes.testing import EXPERIMENTAL_ATCONSTRAINTYPES_INTEGRATION_TESTING  # noqa
from plone import api

import unittest


class TestSetup(unittest.TestCase):
    """Test that experimental.atconstraintypes is properly installed."""

    layer = EXPERIMENTAL_ATCONSTRAINTYPES_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if experimental.atconstraintypes is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'experimental.atconstraintypes'))

    def test_browserlayer(self):
        """Test that IExperimentalAtconstraintypesLayer is registered."""
        from experimental.atconstraintypes.interfaces import (
            IExperimentalAtconstraintypesLayer)
        from plone.browserlayer import utils
        self.assertIn(IExperimentalAtconstraintypesLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = EXPERIMENTAL_ATCONSTRAINTYPES_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['experimental.atconstraintypes'])

    def test_product_uninstalled(self):
        """Test if experimental.atconstraintypes is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'experimental.atconstraintypes'))
