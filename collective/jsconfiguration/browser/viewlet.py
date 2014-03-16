# -*- coding: utf8 -*-

import json
from plone.app.layout.viewlets import ViewletBase
from zope.component import getAdapters
from collective.jsconfiguration.interfaces import IJSONDataProvider, IDOMDataProvider


class JSConfigurationViewlet(ViewletBase):
    """Display JavaScript configuration (JSON or HTML data attributes) in the page"""

    def update(self):
        super(JSConfigurationViewlet, self).update()

    def json_data(self):
        """Load all IJSONDataProvider providers"""
        json_providers = getAdapters((self.context, self.request, self.view), IJSONDataProvider)
        results = []
        for name, provider in json_providers:
            provider.name = name
            results.append(json.dumps(provider()))
        return results

    def dom_data(self):
        """Load all IDOMDataProvider providers"""
        dom_providers = getAdapters((self.context, self.request, self.view), IDOMDataProvider)
        results = []
        for name, provider in dom_providers:
            results.append(provider())
        results = []
