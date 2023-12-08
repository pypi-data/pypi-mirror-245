# -*- coding: utf-8 -*-

# created by marco on 2023/12/8

from setuptools import setup, find_packages

setup(
    name="dbdesigner",
    version="2.0.2",
    packages=find_packages(),
    install_requires=[
        'mysqlclient',
        'psycopg2',
        'pytz',
        'sqlparse'
    ],

    author="chaos-ma",
    author_email="630950058@qq.com",
    description="DBDesigner",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
