from setuptools import setup, find_packages

setup(
    name='cashctrl',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    author='Problemli GmbH',
    #author_email='your.email@example.com',
    description='Python client for the CashCtrl API',
)