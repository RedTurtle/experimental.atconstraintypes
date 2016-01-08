# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import experimental.atconstraintypes


class ExperimentalAtconstraintypesLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        self.loadZCML(package=experimental.atconstraintypes)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'experimental.atconstraintypes:default')


EXPERIMENTAL_ATCONSTRAINTYPES_FIXTURE = ExperimentalAtconstraintypesLayer()


EXPERIMENTAL_ATCONSTRAINTYPES_INTEGRATION_TESTING = IntegrationTesting(
    bases=(EXPERIMENTAL_ATCONSTRAINTYPES_FIXTURE,),
    name='ExperimentalAtconstraintypesLayer:IntegrationTesting'
)


EXPERIMENTAL_ATCONSTRAINTYPES_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(EXPERIMENTAL_ATCONSTRAINTYPES_FIXTURE,),
    name='ExperimentalAtconstraintypesLayer:FunctionalTesting'
)


EXPERIMENTAL_ATCONSTRAINTYPES_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        EXPERIMENTAL_ATCONSTRAINTYPES_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='ExperimentalAtconstraintypesLayer:AcceptanceTesting'
)
