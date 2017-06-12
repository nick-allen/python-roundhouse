==========
Roundhouse
==========


.. image:: https://img.shields.io/pypi/v/roundhouse.svg
    :target: https://pypi.python.org/pypi/roundhouse

.. image:: https://img.shields.io/pypi/pyversions/roundhouse.svg
    :target: https://pypi.python.org/pypi/roundhouse

.. image:: https://img.shields.io/travis/nick-allen/python-roundhouse.svg
    :target: https://travis-ci.org/nick-allen/python-roundhouse

.. image:: https://coveralls.io/repos/github/nick-allen/python-roundhouse/badge.svg?branch=master
    :target: https://coveralls.io/github/nick-allen/python-roundhouse?branch=master

.. image:: https://readthedocs.org/projects/python-roundhouse/badge/?version=latest
    :target: https://python-roundhouse.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

Convert many serialization formats to many formats

----------


Quick Start
-----------

Roundhouse roundtrip serialization

Not sure why you'd do this, but you get the idea

.. code-block:: bash

    echo '{"root": {"nested": {"key": "value"}}}' | \
    rh -i json -o yaml | \
    rh -i yaml -o toml | \
    rh -i toml -o pickle | \
    rh -i pickle -o msgpack | \
    rh -i msgpack -o bson | \
    rh -i bson -o xml | \
    rh -i xml -o json -p

    {
        "root": {
            "nested": {
                "key": "value"
            }
        }
    }


Installation
------------

Installing and extending roundhouse should be painless


Comes with just JSON and Pickle serializers out of the box, only core library dependencies are installed by default

.. code-block:: bash

    pip install roundhouse


Enable one or more additional serializers by installing their dependencies

.. code-block:: bash

    pip install roundhouse[yaml] roundhouse[msgpack] ...


Serializers are enabled automatically if their dependencies are installed, you can also just install them by hand if
you'd prefer

.. code-block:: bash

    pip install roundhouse pyyaml msgpack-python ...


Or quickly install all dependencies for all builtin serializers bundled with core package

.. code-block:: bash

    pip install roundhouse[all]


Usage
-----

Roundhouse can be used as a lightweight CLI or imported in Python as easy to use functions

rh CLI
^^^^^^

The :code:`rh` CLI command is installed automatically, and defaults to reading from stdin and writing stdout

.. code-block:: bash

    echo '{"root": {"nested": {"key": "value"}}}' | rh -i json -o xml -p

    <?xml version="1.0" encoding="utf-8"?>
    <root>
        <nested>
            <key>value</key>
        </nested>
    </root>

Run :code:`rh --help` for full usage instructions

Python
^^^^^^

Data is serialized/deserialized to and from :code:`dict` instances

Other data types may work depending on the serializer format, but are not currently fully supported

Use the :code:`roundhouse.serialize` and :code:`roundhouse.deserialize` functions with target format

.. code-block:: python

    from roundhouse import serialize, deserialize

    data = deserialize('{"root": {"nested": {"key": "value"}}}', 'json')
    print(serialize(data, 'xml', pretty=True))

    '''<?xml version="1.0" encoding="utf-8"?>
    <root>
        <nested>
            <key>value</key>
        </nested>
    </root>'''


Plugins
-------

Additional serializer plugins can be published and installed via pypi/pip using the :code:`roundhouse.serializers`
setuptools entrypoint pointing to module/package containing additional serializer classes

Example :code:`setup.py`:

.. code-block:: python

    from setuptools import setup


    setup(
        name='my_roundhouse_plugin',
        description="My Roundhouse plugin",
        ...
        # Be sure to include any dependencies your serializer(s) may need
        install_requires=[
            ...
        ],
        entry_points={
            # Use the 'roundhouse.serializers' key
            'roundhouse.serializers': [
                # Should point to full importable dot-string path to
                # module or package containing your serializer(s)
                'my_roundhouse_plugin=my_roundhouse_plugin.serializers'
            ]
        },
    )


Matching :code:`my_roundhouse_plugin.serializers` module:

.. code-block:: python

    from roundhouse import Serializer


    class MySerializer(Serializer):

        # Serializer is selected in cli with `rh -i <format> -o`
        # or in python with `serialize(data, '<format>')`

        # Select this serializer with `rh -i my -o ...`
        # or `serialize(data, 'my')` / `deserialize(data, 'my')`
        format = 'my'

        # Optional list of file extensions containing data in
        # serializer format

        # Used by cli to guess format when providing an infile
        # but no explicit `-i <format>`
        extensions = ['.my']

        def serialize(data, stream):
            # Write your serialized bytes data into stream
            # and return it
            stream.write(do_serialization(data))

            return stream

        def deserialize(stream):
            # Read your serialized bytes data out of
            # stream into python object and return it
            data = do_deserialization(stream.read())

            return data

After installing your package, your serializer (and any others that can be found in the module or package you specified)
will be automatically available in the :code:`rh` cli and :code:`serialize` and :code:`deserialize` functions under the
format you specified

Make a great pip-installable serializer plugin? Open an issue to get it listed here!
