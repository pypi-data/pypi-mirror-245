# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['py_tree_sitter_epics']

package_data = \
{'': ['*'],
 'py_tree_sitter_epics': ['tree-sitter-epics/*',
                          'tree-sitter-epics/common/*',
                          'tree-sitter-epics/epics-cmd/*',
                          'tree-sitter-epics/epics-cmd/bindings/node/*',
                          'tree-sitter-epics/epics-cmd/bindings/rust/*',
                          'tree-sitter-epics/epics-cmd/queries/*',
                          'tree-sitter-epics/epics-cmd/src/*',
                          'tree-sitter-epics/epics-cmd/src/tree_sitter/*',
                          'tree-sitter-epics/epics-cmd/test/corpus/*',
                          'tree-sitter-epics/epics-db/*',
                          'tree-sitter-epics/epics-db/bindings/node/*',
                          'tree-sitter-epics/epics-db/bindings/rust/*',
                          'tree-sitter-epics/epics-db/queries/*',
                          'tree-sitter-epics/epics-db/src/*',
                          'tree-sitter-epics/epics-db/src/tree_sitter/*',
                          'tree-sitter-epics/epics-db/test/corpus/*',
                          'tree-sitter-epics/epics-msi-substitution/*',
                          'tree-sitter-epics/epics-msi-substitution/bindings/node/*',
                          'tree-sitter-epics/epics-msi-substitution/bindings/rust/*',
                          'tree-sitter-epics/epics-msi-substitution/queries/*',
                          'tree-sitter-epics/epics-msi-substitution/src/*',
                          'tree-sitter-epics/epics-msi-substitution/src/tree_sitter/*',
                          'tree-sitter-epics/epics-msi-substitution/test/corpus/*',
                          'tree-sitter-epics/epics-msi-template/*',
                          'tree-sitter-epics/epics-msi-template/bindings/node/*',
                          'tree-sitter-epics/epics-msi-template/bindings/rust/*',
                          'tree-sitter-epics/epics-msi-template/queries/*',
                          'tree-sitter-epics/epics-msi-template/src/*',
                          'tree-sitter-epics/epics-msi-template/src/tree_sitter/*',
                          'tree-sitter-epics/epics-msi-template/test/corpus/*',
                          'tree-sitter-epics/snl/*',
                          'tree-sitter-epics/snl/bindings/node/*',
                          'tree-sitter-epics/snl/bindings/rust/*',
                          'tree-sitter-epics/snl/queries/*',
                          'tree-sitter-epics/snl/src/*',
                          'tree-sitter-epics/snl/src/tree_sitter/*',
                          'tree-sitter-epics/snl/test/corpus/*',
                          'tree-sitter-epics/streamdevice-proto/*',
                          'tree-sitter-epics/streamdevice-proto/bindings/node/*',
                          'tree-sitter-epics/streamdevice-proto/bindings/rust/*',
                          'tree-sitter-epics/streamdevice-proto/queries/*',
                          'tree-sitter-epics/streamdevice-proto/src/*',
                          'tree-sitter-epics/streamdevice-proto/src/tree_sitter/*',
                          'tree-sitter-epics/streamdevice-proto/test/corpus/*']}

setup_kwargs = {
    'name': 'py-tree-sitter-epics',
    'version': '0.1.3',
    'description': 'Facilitate tree-sitter-epics parsing in python',
    'long_description': '',
    'author': 'Alexis Gaget',
    'author_email': 'alexis.gaget@cea.fr',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
