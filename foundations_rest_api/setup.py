"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path, environ

here = path.abspath(path.dirname(__file__))
build_version = environ.get('build_version', '0.0.0')

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

package_source = "src"
if environ.get("BUILD_FOUNDATIONS_OBFUSCATED", False):
    package_source = "obfuscated_dist"

setup(
    name='foundations-rest-api',
    version=build_version,
    description='An API for Foundations',
    classifiers=[ 
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
    ],
    install_requires=[
        'dessa_foundations=={}'.format(build_version),
        'foundations_core_rest_api_components=={}'.format(build_version),
        'flask-restful==0.3.6',
        'Flask-Cors==3.0.6',
        'Flask==1.1.0',
        'Werkzeug==0.15.4',
        'pycrypto==2.6.1',
    ],
    packages=find_packages(package_source),
    package_dir={'': package_source},
    package_data={
        'foundations_rest_api': ['resources/*', "**/*pytransform*", "**/license.lic", "*pytransform*", "license.lic", "pytransform.py", "*", "**/*"],
    },
    include_package_data=True
)