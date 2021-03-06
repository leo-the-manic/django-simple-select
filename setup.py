import os
import shutil
import sys
from setuptools import setup

# copy README.rst to README; Github needs .rst, PyPI needs bare
if 'sdist' in sys.argv:
    readme = os.path.join(os.path.dirname(__file__), "README.rst")
    shutil.copyfile(readme, os.path.splitext(readme)[0])

setup(
    name="django-simple-select",
    version='0.2.1',
    description='An autocompleting select widget for Django',
    author='leo-the-manic',
    author_email='manicleo@gmail.com',
    url='https://github.com/leo-the-manic/django-simple-select/',

    packages=['simpleselect'],
    package_data={'simpleselect': ['static/*']},
)
