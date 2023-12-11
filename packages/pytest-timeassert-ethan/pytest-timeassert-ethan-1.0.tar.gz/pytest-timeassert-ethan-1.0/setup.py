# -*- coding: utf-8 -*-
# Author : Ethan
# Time : 2023/12/11 11:06

from setuptools import setup

setup(
    name='pytest-timeassert-ethan',
    url='https://github.com/AomiEthan/pytest-timeassert-ethan',
    version='1.0',
    author="Ethan",
    author_email='995692858@qq.com',
    description='execution duration',
    long_description='assert execution duration using hook',
    classifiers=[
        'Framework :: Pytest',
        'Programming Language :: Python',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python :: 3.6',
    ],
    license='proprietary',
    py_modules=['pytest_timeassert_ethan'],
    keywords=[
        'pytest', 'py.test', 'pytest-timeassert-ethan',
    ],

    install_requires=[
        'pytest'
    ],
    entry_points={
        'pytest11': [
            'timeassert = pytest_timeassert_ethan',
        ]
    }
)
