from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()


VERSION = '2023.12.08'
DESCRIPTION = 'Automatization'
LONG_DESCRIPTION = 'A package that allows other people to play Jackbox Party Packs like 24/7'

# Setting up
setup(
    name="JPB",
    version=VERSION,
    author="Loamf",
    author_email="<loamf2@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['opencv-python', 'pyautogui', 'numpy'],
    keywords=['python', 'jackbox', 'automatization', 'jackbox24'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)
