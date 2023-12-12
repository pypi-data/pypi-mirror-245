from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='python-modelsonic',
    version='0.1.0',
    description='A Python package for working with ModelSonic APIs',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author_email='sirjanpreet.ext@writesonic.com',
    packages=['modelsonic'],
    install_requires=[
        'httpx>=0.25.2',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)