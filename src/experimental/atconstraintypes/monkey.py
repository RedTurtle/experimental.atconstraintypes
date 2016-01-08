# -*- coding: utf-8 -*-
from Products.ATContentTypes.lib.constraintypes import DISABLED
from Products.ATContentTypes.lib.constraintypes import ENABLED
from Products.ATContentTypes.lib.constraintypes import ACQUIRE
from Products.ATContentTypes.lib.constraintypes import getParent
from Products.ATContentTypes.lib.constraintypes import parentPortalTypeEqual
from Products.CMFCore.PortalFolder import PortalFolderBase as PortalFolder
from Products.CMFPlone.interfaces.constrains import ISelectableConstrainTypes
from Acquisition import aq_parent
from Acquisition import aq_inner


def allowedContentTypes(self, context=None):
    """
    returns constrained allowed types as list of fti's.
    There is a try/except for handle AT folders inside DX containers
    """
    if context is None:
        context = self
    mode = self.getConstrainTypesMode()

    # Short circuit if we are disabled or acquiring from non-compatible
    # parent

    parent = getParent(self)
    if mode == DISABLED or (mode == ACQUIRE and not parent):
        return PortalFolder.allowedContentTypes(self)
    elif mode == ACQUIRE and not parentPortalTypeEqual(self):
        globalTypes = self.getDefaultAddableTypes(context)
        if parent.portal_type == 'Plone Site':
            return globalTypes
        else:
            try:
                allowed = list(parent.getLocallyAllowedTypes(context))
            except AttributeError:
                # parent is a DX content?
                behavior = ISelectableConstrainTypes(parent)
                if not behavior:
                    # return context addable types
                    return get_context_ftis(self)
                allowed = behavior.getLocallyAllowedTypes(context)
            return [fti for fti in globalTypes if fti.getId() in allowed]
    else:
        return get_context_ftis(self)


def get_context_ftis(context):
    globalTypes = context.getDefaultAddableTypes(context)
    allowed = list(context.getLocallyAllowedTypes())
    ftis = [fti for fti in globalTypes if fti.getId() in allowed]
    return ftis


def getLocallyAllowedTypes(self, context=None):
    """
    There is a try/except for handle AT folders inside DX containers
    """
    if context is None:
        context = self
    mode = self.getConstrainTypesMode()

    if mode == DISABLED:
        return [fti.getId() for fti in self.getDefaultAddableTypes(context)]
    elif mode == ENABLED:
        return self.getField('locallyAllowedTypes').get(self)
    elif mode == ACQUIRE:
        parent = getParent(self)
        if not parent or parent.portal_type == 'Plone Site':
            return [fti.getId() for fti in self.getDefaultAddableTypes(context)]
        elif not parentPortalTypeEqual(self):
            # if parent.portal_type != self.portal_type:
            default_addable_types = [fti.getId() for fti in self.getDefaultAddableTypes(context)]
            try:
                locally_allowed_types = parent.getLocallyAllowedTypes(context) if ISelectableConstrainTypes.providedBy(parent) else parent.getLocallyAllowedTypes()
            except AttributeError:
                # parent is a DX content?
                behavior = ISelectableConstrainTypes(parent)
                if not behavior:
                    # return context default addable types
                    return default_addable_types
                locally_allowed_types = behavior.getLocallyAllowedTypes(context) if ISelectableConstrainTypes.providedBy(parent) else behavior.getLocallyAllowedTypes()
            return [t for t in locally_allowed_types
                    if t in default_addable_types]
        else:
            if ISelectableConstrainTypes.providedBy(parent):
                return parent.getLocallyAllowedTypes(context)
            else:
                return parent.getLocallyAllowedTypes()
    else:
        raise ValueError, "Invalid value for enableAddRestriction"

def getImmediatelyAddableTypes(self, context=None):
    """Get the list of type ids which should be immediately addable.
    If enableTypeRestrictions is ENABLE, return the list set; if it is
    ACQUIRE, use the value from the parent; if it is DISABLE, return
    all type ids allowable on the item.
    There is a try/except for handle AT folders inside DX containers
    """
    if context is None:
        context = self
    mode = self.getConstrainTypesMode()

    if mode == DISABLED:
        return [fti.getId() for fti in self.getDefaultAddableTypes(context)]
    elif mode == ENABLED:
        return self.getField('immediatelyAddableTypes').get(self)
    elif mode == ACQUIRE:
        parent = getParent(self)
        if not parent or parent.portal_type == 'Plone Site':
            return [fti.getId() for fti in
                    PortalFolder.allowedContentTypes(self)]
        elif not parentPortalTypeEqual(self):
            default_allowed = [fti.getId() for fti in
                               PortalFolder.allowedContentTypes(self)]
            try:
                immediately_addable = parent.getImmediatelyAddableTypes(context)
            except AttributeError:
                # parent is a DX content?
                behavior = ISelectableConstrainTypes(parent)
                if not behavior:
                    # return context default addable types
                    immediately_addable = self.getField('immediatelyAddableTypes').get(self)
                immediately_addable = behavior.getImmediatelyAddableTypes(context)
            return [t for t in immediately_addable if t in default_allowed]
        else:
            parent = aq_parent(aq_inner(self))
            try:
                return parent.getImmediatelyAddableTypes(context)
            except AttributeError:
                # parent is a DX content?
                behavior = ISelectableConstrainTypes(parent)
                if not behavior:
                    # return context default addable types
                    return self.getField('immediatelyAddableTypes').get(self)
                return behavior.getImmediatelyAddableTypes(context)
    else:
        raise ValueError, "Invalid value for enableAddRestriction"
