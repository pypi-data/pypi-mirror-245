# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mcglm']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.5.2,<4.0.0',
 'numpy>=1.25,<2.0',
 'pandas>=1.3.3,<2.0.0',
 'patsy>=0.5.2,<0.6.0',
 'statsmodels>=0.13.2,<0.14.0']

setup_kwargs = {
    'name': 'mcglm',
    'version': '0.2.3',
    'description': 'Multivariate Covariance Generalized Linear Models',
    'long_description': '### Multivariate Covariance Generalized Linear Models\n\nhttps://pypi.org/project/mcglm/\n\nThe mcglm package brings to python language one of the most powerful extensions to GLMs(Nelder, Wedderburn; 1972), the Multivariate Covariance Generalized Linear Models(Bonat, Jørgensen; 2016).\n\nThe GLMs have consolidated as a unified statistical model for analyzing non-gaussian independent data throughout the years. Notwithstanding enhancements to Linear Regression Models(Gauss), some key assumptions, such as the independence of components in the response, each element of the target belonging to an exponential dispersion family maintains.\n\nMCGLM aims to expand the GLMs by allowing fitting on a wide variety of inner-dependent datasets, such as spatial and longitudinal, and supplant the exponential dispersion family output by second-moment assumptions(Wedderburn; 1974)\n\nhttps://jeancmaia.github.io/posts/tutorial-mcglm/tutorial_mcglm.html\n\n-----\n\nThe mcglm python package follows the standard pattern of the statsmodels library and aims to be another API on the package. Therefore, Python machine learning practitioners will be very familiar with this new statistical model. \n\n\nTo install this package, use \n\n```bash\npip install mcglm\n```\n\nTutorial MCGLM instills on the library usage by a wide-variety of examples(https://jeancmaia.github.io/posts/tutorial-mcglm/tutorial_mcglm.html). The following code snippet shows the model fitting for a Gaussian regression analysis.\n\n```python\nmodelresults = MCGLM(endog=y, exog=X).fit()\n\nmodelresults.summary()\n```\n\n',
    'author': 'Jean Carlos Faoot Maia',
    'author_email': 'jeanclmaia@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9',
}


setup(**setup_kwargs)
