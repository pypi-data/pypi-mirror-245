# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_code']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'django-code',
    'version': '0.1.0',
    'description': '',
    'long_description': '# Django Code',
    'author': 'Paris Kasidiaris',
    'author_email': 'paris@withlogic.co',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
