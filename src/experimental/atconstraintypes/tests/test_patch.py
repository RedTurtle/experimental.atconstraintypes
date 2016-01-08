# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from experimental.atconstraintypes.testing import EXPERIMENTAL_ATCONSTRAINTYPES_INTEGRATION_TESTING  # noqa
from plone import api
from plone.app.testing import TEST_USER_ID, setRoles
from plone.dexterity.fti import DexterityFTI
import unittest


def add_dx_folder_type(portal):
    fti = DexterityFTI('dx_folder')
    portal.portal_types._setObject('dx_folder', fti)
    fti.klass = 'plone.dexterity.content.Container'
    fti.filter_content_types = False
    fti.behaviors = (
        'Products.CMFPlone.interfaces.constrains.'
        'ISelectableConstrainTypes',
        'plone.app.dexterity.behaviors.metadata.IBasic')
    return fti


class TestPatch(unittest.TestCase):
    """Test that experimental.atconstraintypes is properly installed."""

    layer = EXPERIMENTAL_ATCONSTRAINTYPES_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.fti = add_dx_folder_type(self.portal)
        self.portal.invokeFactory('dx_folder', 'dx-folder')
        self.dx_folder = self.portal['dx-folder']
        self.dx_folder.invokeFactory("Folder", id='at-folder')
        self.at_folder = self.dx_folder['at-folder']


    def test_acquire_from_dx_parent(self):
        #
        # # Let folder use a restricted set of types
        # self.portal.portal_types.Folder.filter_content_types = 1
        # self.portal.portal_types.Folder.allowed_content_types = \
        #     ('Document', 'Image', 'News Item', 'Topic', 'Folder')
        #
        # # Set up outer folder with restrictions enabled
        # self.af.setConstrainTypesMode(constraintypes.ENABLED)
        # self.af.setLocallyAllowedTypes(['Folder', 'Image'])
        # self.af.setImmediatelyAddableTypes(['Folder', 'Image'])
        #
        # # Create inner type to acquire (default)
        # self.af.invokeFactory('Folder', 'outer', title='outer')
        # outer = self.af.outer
        #
        # outer.invokeFactory('Folder', 'inner', title='inner')
        # inner = outer.inner
        #
        # inner.setConstrainTypesMode(constraintypes.ACQUIRE)
        #
        # # Test persistence
        # inner.setLocallyAllowedTypes(['Document', 'Event'])
        # inner.setImmediatelyAddableTypes(['Document'])
        #
        # self.assertEqual(inner.getRawLocallyAllowedTypes(),
        #                         ('Document', 'Event',))
        # self.assertEqual(inner.getRawImmediatelyAddableTypes(),
        #                         ('Document',))
        #
        # # Fail - we didn't acquire this, really, since we can't acquire
        # # from parent folder of different type
        # self.assertRaises(ValueError, inner.invokeFactory, 'Topic', 'a')
        # self.assertFalse('News Item' in inner.getLocallyAllowedTypes())
        #
        # # Make sure immediately-addable are set to default
        # self.assertEqual(inner.getImmediatelyAddableTypes(),
        #                  inner.getLocallyAllowedTypes())
        # self.assertEqual(inner.allowedContentTypes(), outer.allowedContentTypes())
        #
        # # Login the new user
        # self.portal.acl_users._doAddUser('restricted', 'secret', ['Member'], [])
        # inner.manage_addLocalRoles('restricted', ('Manager',))
        # user = self.portal.acl_users.getUserById('restricted')
        # newSecurityManager(None, user)
        # self.assertEqual([t.getId() for t in inner.allowedContentTypes()],
        #                      ['Folder', 'Image'])
