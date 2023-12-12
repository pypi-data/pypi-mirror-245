from setuptools import setup, find_packages

setup(
    name='Superman123',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'scikit-learn',
        'matplotlib',
        'numpy',
        'pandas',
    ],
)
