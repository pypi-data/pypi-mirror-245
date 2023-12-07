"""
Pypi deployment guide :

pip install setuptools, wheel, twine

py setup.py sdist bdist_wheel
twine upload dist/*
user : __token__
password : <upload_token>
"""

from setuptools import setup
import os

here = os.path.abspath(os.path.dirname(__file__))

VERSION = '0.0.1'
DESCRIPTION = 'Photoshop Object Model Session'
LONG_DESCRIPTION = r"""
This package is designed to interact with Photoshop using its Component Object Model using python.
the class PhotoshopSession be used as a context, who handles errors while providing autocompletion, access to docstrings, and accurate type hints in your preferred IDE.

Usage : 
'''python
from photoshop_object_model_session import PhotoshopSession

with PhotoshopSession() as ps:
    print(ps.Application.Version)
    new_layer = ps.Application.ActiveDocument.ArtLayers.Add()
    new_layer.Name = "Hello World"
'''

All classes have been written based on Photoshop's VBS documentation, which can be found at <https://github.com/Adobe-CEP/CEP-Resources/blob/master/Documentation/Product%20specific%20Documentation/Photoshop%20Scripting/photoshop-vbs-ref-2020.pdf>.
As such, the code you'll find here isn't very pythonic, because it is based on the Visual Basic syntax.
Please note that this package may contain inconsistencies, missing return types, and typos. Unfortunately, most of these issues stem from faithfully transcribing Adobes's flawed documentation.
"""

# Setting up
setup(
    name="photoshop-object-model-session",
    version=VERSION,
    author="Tristan Languebien",
    author_email="<tlanguebien@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=['photoshop_object_model_session'],
    install_requires=['pywin32', 'photoshop-object-model'],
    keywords=['python', 'photoshop'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)