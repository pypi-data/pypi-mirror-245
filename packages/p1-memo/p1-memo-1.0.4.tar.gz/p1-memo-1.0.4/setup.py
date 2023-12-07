import os
from distutils.core import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

setup(
    name='p1-memo',
    version='1.0.4',
    description='Forked from PyMemoize',
    long_description='README.md',
    long_description_content_type='text/markdown',
    url='http://github.com/mikeboers/PyMemoize',
    
    packages=['memoize'],
    
    author='Dekoruma',
    author_email='engineering@dekoruma.com',
    license='BSD-3',
    
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    
)
