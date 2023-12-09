import os
from setuptools import setup, find_packages

import yydict

here = os.path.abspath(os.path.dirname(__file__))

SHORT = 'YYDict is a dictionary whose items can be set using both attribute and item syntax.'

with open(os.path.join(here, 'README.rst')) as f1, open(os.path.join(here, 'CHANGES')) as f2:
    LONG = f1.read() + '\n\n' + f2.read()

    for_more_detail_info = "For more info check out the README at 'https://gitee.com/changyubiao/yydict'."
    LONG += '\n\n' + for_more_detail_info

setup(
    name='yydict',
    version=yydict.__version__,
    packages=find_packages('.'),
    url='https://gitee.com/changyubiao/yydict',
    download_url="https://pypi.python.org/project/yydict/",
    author=yydict.__author__,
    author_email='15769162764@163.com',
    keywords=['Tools'],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    include_package_data=True,
    description=SHORT,
    long_description=LONG,
    test_suite='test_yydict',
    package_data={'': ['LICENSE']}
)
