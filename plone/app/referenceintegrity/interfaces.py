from zope.interface import Interface
from zope.schema import List
from zope.schema import TextLine


class ISettings(Interface):

    reference_types = List(
        title=u"Reference types",
        description=u"Reference types that should be protected",
        required=False,
        value_type=TextLine())
