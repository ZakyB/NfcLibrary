from setuptools import setup, find_packages

setup(
    name='nfc_library',
    version='0.1.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'requests',
    ],
)
