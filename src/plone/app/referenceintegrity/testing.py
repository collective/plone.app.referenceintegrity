from plone.app.testing import PloneWithPackageLayer
from plone.app.testing import IntegrationTesting
import plone.app.referenceintegrity


REFERENCE_INTEGRITY = PloneWithPackageLayer(zcml_filename="configure.zcml",
    zcml_package=plone.app.referenceintegrity,
    gs_profile_id='plone.app.referenceintegrity:default',
    name="REFERENCE_INTEGRITY")

INTEGRATION_REFERENCE_INTEGRITY = IntegrationTesting(
    bases=(REFERENCE_INTEGRITY,),
    name="INTEGRATION_REFERENCE_INTEGRITY")
