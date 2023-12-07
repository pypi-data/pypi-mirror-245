# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ml_switching_reg']

package_data = \
{'': ['*'], 'ml_switching_reg': ['saved_models/plots/*']}

install_requires = \
['linearmodels==4.26',
 'matplotlib==3.4.3',
 'numba-stats==1.1.0',
 'numpy==1.24.2',
 'pandas==1.4.2',
 'patsy==0.5.2',
 'scikit-learn==1.2.1',
 'scipy==1.8.0',
 'statsmodels==0.13.2',
 'tqdm==4.56.0']

setup_kwargs = {
    'name': 'ml-switching-reg',
    'version': '0.4.14',
    'description': 'A robust estimator to machine learning prediction misclassification',
    'long_description': 'None',
    'author': 'Aleksandr Michuda',
    'author_email': 'amichuda@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
