#!/usr/bin/env python
from setuptools import setup

if __name__ == '__main__':
    setup(
        name = 'django-tastypie-ext',
        version = '0.1',
        description = "Various tastypie extensions, authentication methods, etc.",
        long_description = open('README.rst', 'r').read(),
        author = 'Adam Ever-Hadani',
        author_email = 'adamhadani@gmail.com',
        url = 'https://github.com/adamhadani/django-tastypie-ext',
        keywords = "django tastypie api restful",
        license = 'Apache 2.0',

        packages = ('tastypie_ext',),

        zip_safe = False,

        install_requires = (
            'Django>=1.4',
            'django-tastypie>=0.9.11',
        ),
    )
