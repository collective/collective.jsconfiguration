# -*- coding: utf8 -*-

from zope.interface import Interface
from zope.interface import Attribute


class IJSConfigurationLayer(Interface):
    """Marker interface for collective.jsconfiguration browser layer"""


class IJSDataProvider(Interface):
    """Generic interface for a callable object able to provide JavaScript configuration data"""

    name = Attribute("""Name of the provider (if any)""")
    context = Attribute("""The Plone context""")
    request = Attribute("""The Zope request""")
    view = Attribute("""The current view""")


class IJSONDataProvider(IJSDataProvider):
    """An object that provide JSON configuration data"""


class IDOMDataProvider(IJSDataProvider):
    """An object that provide configuration data through HTML 5 data attributes"""