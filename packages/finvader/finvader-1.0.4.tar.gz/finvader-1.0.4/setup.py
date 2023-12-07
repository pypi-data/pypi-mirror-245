# -*- coding: utf-8 -*


import setuptools

with open("README.md", "r") as fh:
    description = fh.read()

    setuptools.setup(
        name="finvader",
        version="1.0.4",
        author="Petr Koráb",
        author_email="xpetrkorab@gmail.com",
        packages=["finvader"],
        description="VADER sentiment classifier updated with financial lexicons",
        long_description=description,
        long_description_content_type="text/markdown",
        url="https://github.com/PetrKorab/FinVADER",
        python_requires='>=3.8, <3.12',
        install_requires = ['nltk==3.6.2'],
        license='OSI Approved :: Apache Software License'
    )