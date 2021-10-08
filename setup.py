# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in mobile_backend/__init__.py
from mobile_backend import __version__ as version

setup(
	name='mobile_backend',
	version=version,
	description='Mobile Backend',
	author='Omar',
	author_email='mobile_backend@frappe.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
