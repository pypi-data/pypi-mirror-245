import pathlib
from setuptools import setup
from untanglepyut import __version__ as untanglepyutVersion

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()
LICENSE = (HERE / 'LICENSE').read_text()

setup(
    name="untanglepyut",
    version=untanglepyutVersion,
    author_email='Humberto.A.Sanchez.II@gmail.com',
    description='XML to Ogl Object Model',
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/hasii2011/untanglepyut",
    packages=[
        'untanglepyut',
    ],
    package_data={
        'untanglepyut': ['py.typed'],
    },

    install_requires=[
        'untangle==1.2.1',
        'codeallybasic==0.5.2',
        'codeallyadvanced==0.5.2',
        'pyutmodelv2==2.0.0a4',
        'ogl==2.0.0a4',
    ],
)