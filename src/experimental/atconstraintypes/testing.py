# -*- coding: utf-8 -*-
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2
import plone.app.dexterity

import experimental.atconstraintypes


class ExperimentalAtconstraintypesLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        self.loadZCML(package=experimental.atconstraintypes)
        self.loadZCML(name='meta.zcml', package=plone.app.dexterity)
        self.loadZCML(package=plone.app.dexterity)

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'plone.app.dexterity:testing')


EXPERIMENTAL_ATCONSTRAINTYPES_FIXTURE = ExperimentalAtconstraintypesLayer()


EXPERIMENTAL_ATCONSTRAINTYPES_INTEGRATION_TESTING = IntegrationTesting(
    bases=(EXPERIMENTAL_ATCONSTRAINTYPES_FIXTURE,),
    name='ExperimentalAtconstraintypesLayer:IntegrationTesting'
)


EXPERIMENTAL_ATCONSTRAINTYPES_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(EXPERIMENTAL_ATCONSTRAINTYPES_FIXTURE,),
    name='ExperimentalAtconstraintypesLayer:FunctionalTesting'
)
