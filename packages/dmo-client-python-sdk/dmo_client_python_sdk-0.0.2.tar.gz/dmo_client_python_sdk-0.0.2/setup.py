#############################################
# File Name: setup.py
# Author: thao
# Mail: thao92@126.com
# Created Time:  2020-08-05 11:08:34
#############################################


from setuptools import setup, find_packages
import sys
import importlib

importlib.reload(sys)

setup(
    name="dmo_client_python_sdk",
    version="0.0.2",
    keywords=["pip", "dmo_client_python_sdk", "liuxb", "sdk"],
    description="Encapsulateing Interface",
    long_description=" Encapsulating Interface",
    license="MIT Licence",

    url="https://gitlab.sanywind.net/bigdata/dmo-client-python-sdk",
    author="liuxb",
    author_email="llxiangbin@163.com",
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=['requests', 'pandas', 'retry']
)