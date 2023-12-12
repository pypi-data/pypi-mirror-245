from setuptools import setup, find_packages

setup(
	name='s3-storage-stats',
	version='1.0.1',
	author='Alyssa Blair',
	author_email='alyssablair@uvic.ca',
	packages=['s3_storage_stats'],
	install_requires=['boto3>=1.2.8'],
	scripts=['s3-storage-stats'],
)
