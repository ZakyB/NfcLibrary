# setup.py

from setuptools import setup, find_packages

setup(
    name='nfc_library',
    version='0.1.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'nfcpy',  # ou toute autre dépendance nécessaire
    ],
    entry_points={
        'console_scripts': [
            'nfc_library=nfc_library.__main__:main',
        ],
    },
)
