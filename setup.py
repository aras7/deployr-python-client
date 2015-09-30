try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name="deployrclient",
    version="0.0.1",
    author="Andres Arrieche",
    author_email="andres.arrieche@telefonica.com",
    description="Python client for deployr",
    packages=["."],
    url="https://github.com/aras7/deployr-python-client",
    install_requires=["requests"],
    license="Apache",
    classifiers=["Programming Language :: Python", "License :: OSI Approved :: Apache Software License"]
)
