# -*- coding: utf-8 -*-
"""
Created on Sun Dec 10 00:07:44 2023

@author: Stacey.Yang
"""
from setuptools import setup,find_packages

setup(
    name='CRFActions',
    version='1.7',
    packages=find_packages(),
    install_requires=[
        'openpyxl',
        'pandas',
        'pdfplumber',
        'tkinter'
    ],
    author='Stacey',
    author_email='yq13408614660@163.com',
    description='Package for processing CRF',
    python_requires='>=3.6'
)