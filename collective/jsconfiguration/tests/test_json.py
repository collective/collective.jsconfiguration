# -*- coding: utf-8 -*-

import unittest
from collective.jsconfiguration.interfaces import IJSConfigurationLayer
from collective.jsconfiguration.interfaces import IJSONDataProvider
from collective.jsconfiguration.testing import JS_CONFIGURATION_INTEGRATION_TESTING
from collective.jsconfiguration.tests.base import BaseTestCase
from zope.interface import implements
from zope.interface import Interface
from zope.component import getMultiAdapter
from zope.component import queryUtility
from zope.component import provideAdapter
from zope.publisher.interfaces.browser import IHTTPRequest


class JSONConfiguration(object):
    implements(IJSONDataProvider)
    
    def __init__(self, context, request, view):
        self.name = u''
        self.context = context
        self.request = request
        self.view = view
        
    def __call__(self):
        return {'name' : self.name}


class TestJSON(BaseTestCase):

    layer = JS_CONFIGURATION_INTEGRATION_TESTING

    def setUp(self):
        super(TestJSON, self).setUp()
        provideAdapter(
                JSONConfiguration,
                (Interface,
                 IHTTPRequest,
                 Interface),
                provides=IJSONDataProvider,
                name=u'foo.json.data'
            )

    def test_configurtion_in_page(self):
        portal = self.layer['portal']
        self.assertTrue("""<script type="text/collective.jsconfiguration.json">"""
                        """{"name": "foo.json.data"}</script>""" in portal())


