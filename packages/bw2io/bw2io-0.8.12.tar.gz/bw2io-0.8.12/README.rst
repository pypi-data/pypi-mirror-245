Brightway2 input and output
===========================

.. image:: https://img.shields.io/pypi/v/bw2io.svg
   :target: https://pypi.org/project/bw2io/
   :alt: pypi version

.. image:: https://img.shields.io/conda/vn/conda-forge/bw2io.svg
   :target: https://anaconda.org/conda-forge/bw2io
   :alt: conda-forge version

.. image:: https://dev.azure.com/mutel/Brightway%20CI/_apis/build/status/brightway-lca.brightway2-io?branchName=bw2legacy
   :target: https://dev.azure.com/mutel/Brightway%20CI/_build?definitionId=5&_a=summary&repositoryFilter=3&branchFilter=113
   :alt: azure build status

This package provides tools for the import, export, and management of inventory databases and impact assessment methods. It is part of the `Brightway2 LCA framework <https://brightwaylca.org>`_. `Online documentation <https://docs.brightwaylca.org/>`_ is available, and the source code is hosted on `Bitbucket <https://bitbucket.org/cmutel/brightway2-io>`_.

In contrast with previous IO functionality in Brightway2, brightway2-io uses an iterative approach to importing and linking data. First, data is *extracted* into a common format. Next, a series of *strategies* is employed to uniquely identify each dataset and link datasets internally and to the biosphere. Following internal linking, linking to other background datasets can be performed. Finally, database data is written to disk.

This approach offers a number of benefits that help mitigate some of the serious problems in existing inventory data formats: the number of unlinked exchanges can be easily seen, linking strategies can be iteratively applied, and intermediate results can be saved.

Here is a typical usage:

.. code-block:: python

    In [1]: from bw2io import *

    In [2]: so = SingleOutputEcospold2Importer("/path/to/ecoinvent/3.1/cutoff/datasets", "ecoinvent 3.1 cutoff")
    11301/11301 (100%) |||||||||||||||||||||||||||||||||||||||||||||||||||||||||| Time: 0:01:56
    Converting to unicode
    Extracted 11301 datasets in 262.63 seconds

    In [3]: so.apply_strategies()
    Applying strategy: remove_zero_amount_coproducts
    Applying strategy: remove_zero_amount_inputs_with_no_activity
    Applying strategy: es2_assign_only_product_with_amount_as_reference_product
    Applying strategy: assign_single_product_as_activity
    Applying strategy: create_composite_code
    Applying strategy: link_biosphere_by_flow_uuid
    Applying strategy: link_internal_technosphere_by_composite_code
    Applying strategy: delete_exchanges_missing_activity
    Applying strategy: delete_ghost_exchanges
    Applying strategy: mark_unlinked_exchanges

    In [4]: so.statistics()
    11301 datasets
    521712 exchanges
    0 unlinked exchanges
    Out[4]: (11301, 521712, 0)

    In [5]: so.write_database()

Note that brightway2-io can't magically make problems in databases go away.
