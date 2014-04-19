.. contents:: **Table of contents**

Introduction
============

This product is targeted to developer who need to distribute JavaScript configuration data or
i18n strings with their Plone products.

Data injected in the page could be taken from whatever server side configuration setting you want
(most of the time from Plone registry).

How it works
============

A new viewlet will be registered in the HTML head of the site. This viewlet is normally empty and will
do nothing until a 3rd party product will register new ``IJSDataProvider`` adapters.

There are three subtypes of adapters, choosing one of them depends on what you want to reach in your
add-on. Registering *named adapters* is recommended, in that way override the registration will be possible.
In the case of ``IJSObjectDataProvider`` the name is required because it's used as name of the defined
variable (see below).

IJSONDataProvider
-----------------

Use it when you want to add new JavaScript data in the form of a JSON *template*.

The adapter must be a callable object that return a string that could be threat as a JSON
string. It will be added to the page in a ``script`` of type "text/collective.jsconfiguration.json".

For example:

.. code-block:: xml

    <script type="text/collective.jsconfiguration.json"
            id="your_adapter_name_if_any">
        {"foo": ... }
    </script>

IDOMDataProvider
----------------

Use it when you want to add new JavaScript data in the form of XML nodes.

The adapter must be a callable object that return something you want to be put inside the page.
It will be added to the page in a ``script`` of type "text/collective.jsconfiguration.xml".

An example:

.. code-block:: xml

    <script type="text/collective.jsconfiguration.xml"
            id="your_adapter_name_if_any">
        <foo data-i18n-label1="Benvenuto"
             data-i18n-label2="Questo è un esempio di traduzione">
             ...
        </foo>
    </script>

Although there's no real limitation in using this provider, it has been designed for injecting
XML sub-DOM.
If the callable use a template to render it's content you can use a browser view.
This can be *really* useful for internationalization of your JavaScript interface (because
you can then rely on Zope i18n support and tools like `i18ndude`__).

__ http://pypi.python.org/pypi/i18ndude

IJSObjectDataProvider
---------------------

Use it when you want to add new JavaScript data in the form of a plain JavaScript object
assigned to a variable. For this reason the data will be used in a standard ``script``
tag.

This is very similar to the ``IJSONDataProvider`` above (the callable must return a valid JSON string)
but with some important differences:

* a name for the adapter is required
* the name of the adapter will be used as variable name to which the data will be assigned

If the name will be dotted, a nested JavaScript objects structure will be created.

An example for an adapter called "``foo.bar``":

.. code-block:: javascript

    <script type="text/javascript">
    if (typeof foo==='undefined') {
        foo = {};
    }
    
    foo.bar = {"foo": "Hello World"};
    </script>

Registering a new configuration
===============================

Whatever is your choice, you simply need to register an adapter that adapts the **current context**,
the **request** and the **current view**.

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
layers is registered (commonly: your add-on product is installed) and only when a specific view is called.

As far as the adapter registration is using the same name of the first example, the last registration will
override the first when applicable.

Finally, there's the adapter class::

.. code-block:: python

    class YourXMLAdapter(object):
        implements(IDOMDataProvider)
        
        def __init__(self, context, request, view):
            self.context = context
            self.request = request
            self.view = view
            
        def __call__(self):
            ...
