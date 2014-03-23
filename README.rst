.. contents:: **Table of contents**

Introduction
============

This product is targeted to developer who need to distribute JavaScript configuration data or
i18n strings with products.

Data injected in the page could be taken from whatever server side configuration setting you want
(for example: a Plone registry set).

How it works
============

A new viewlet will be registered in the head on the Plone site. This viewlet is normally empty and will
do nothing until a 3rd party product will register new ``IJSDataProvider`` adapters.

There are two subtypes of this adapter:

``IJSONDataProvider``
    when you want to add new JavaScript data in the form of JSON
``IDOMDataProvider``
    when you want to add new JavaScript data in the form of XML nodes

Registering a new configuration
-------------------------------

Whatever is your choice, you simply need to register an adapter that adapts the **current context**,
the **request** and the **current view**.
Registering a *named adapter* is highly recommended; in that way override the registration will be possible.

An example:

.. code-block:: xml

   <adapter
       factory="your.package.adapter.YourXMLAdapter"
       provides="collective.jsconfiguration.interfaces.IDOMDataProvider"
       for="* * *"
       name="your_zml_configuration"
       />

In the example above the configuration will be added to every page of the site.

.. code-block:: xml

   <adapter
       factory="your.package.adapter.AnotherXMLAdapter"
       provides="collective.jsconfiguration.interfaces.IDOMDataProvider"
       for="Products.CMFPlone.interfaces.siteroot.IPloneSiteRoot
            your.package.browser.interfaces.IYourProductLayer
            your.package.browser.interfaces.IYourSpecialView"
       name="your_zml_configuration"
       />

In the last example another configuration will only added to the site root, only when a 3rd party browser
layers is registered (commonly: you add-on product is installed) and only when a specific view is called.

As far as the adapter registration is using the same name of the first example, the last registration will
override the first when displayed.

