from setuptools import setup, find_packages
from mathpy.common import module_version as version
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "todo.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

DESCRIPTION = 'MathPy Project Programming language'

# Setting up
setup(
    name="mathpy-string",
    version=version,
    author="Joyful-Bard",
    author_email="<thisis@notarealemail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    package_data={'mathpy': [
            'language_grammar/token_types.json',
            'language_grammar/keywords.json',
    ]},
    install_requires=[],
    keywords=['mathpy', 'script', 'language'],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)