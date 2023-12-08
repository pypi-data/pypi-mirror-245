from setuptools import setup, find_packages

setup(
    name='waxdispatcherhelper',
    version='0.0.1',
    description='Utilities to help with setting up transactions with waxnftdispatcher',
    author='Funkaclau',
    author_email='cloudspg@gmail.com',
    packages=['waxdispatcherhelper'],
    install_requires=[
        'requests',
		  'waxnftdispatcher'
    ],
    include_package_data=True
)
